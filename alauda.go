package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "os"
)

type Detil struct {
    Image string
    Uuid  string
    Port  []int
}

func getBody(url string) []uint8 {
    client := &http.Client{}
    request, err := http.NewRequest("GET", url, nil)
    if err != nil {
        log.Println(err)
        return nil
    }
    request.Header.Add("Authorization", "Token xxxxxxxxxx")
    resp, err := client.Do(request)

    // fmt.Printf("%d", resp.StatusCode)

    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        log.Println(err)
        return nil
    } else {
        return body
    }
}

func getServicePort(port_body []uint8) []int {
    type ServiceResult struct {
        Ports []int `json:"ports"`
    }
    service_result := &ServiceResult{}
    json.Unmarshal(port_body, service_result)
    if len(service_result.Ports) > 0 {
        fmt.Println(service_result.Ports[0])
    }
    return service_result.Ports
}

func getServiceMap(body []uint8) map[string]Detil {
    var port_body []uint8
    var port_value []int
    port_url_basic := "https://api.alauda.cn/v1/services/hbykt/"
    type Service struct {
        ServiceName string `json:"service_name"`
        ImageName   string `json:"image_name"`
        ImageTag    string `json:"image_tag"`
        Uuid        string `json:"uuid"`
    }

    type Result struct {
        Count   int
        Results []Service
    }
    // fmt.Printf("body type: %T \n", body)
    serviceMap := make(map[string]Detil)
    result := &Result{}
    // 返回状态为1表示正常：result.Status == "1"
    json.Unmarshal(body, result) //解析json字符串
    for i := 0; i < len(result.Results); i++ {
        // for i := 0; i < 3; i++ {
        port_body = getBody(port_url_basic + result.Results[i].Uuid)
        port_value = getServicePort(port_body)
        // fmt.Println(result.Results[i].ServiceName)
        // fmt.Println(result.Results[i].ImageName + ":" + result.Results[i].ImageTag)
        // serviceMap[result.Results[i].ServiceName] = result.Results[i].ImageName + ":" + result.Results[i].ImageTag
        serviceMap[result.Results[i].ServiceName] = Detil{result.Results[i].ImageName + ":" + result.Results[i].ImageTag, result.Results[i].Uuid, port_value}
    }
    return serviceMap
}

func main() {

    service_url := "https://api.alauda.cn/v1/services/hbykt?region_name=testing_clusers&project_name=default"
    body := getBody(service_url)

    //服务及镜像列表以json形式写入文件
    serviceMap := getServiceMap(body)
    serviceMapJson, _ := json.Marshal(serviceMap)
    if ioutil.WriteFile("list.json", serviceMapJson, os.ModeAppend) == nil {
        fmt.Println("文件写入成功")
    }
    //查询服务是否存在
    find_app, ok := serviceMap["x-wechat"]
    if ok {
        fmt.Println("服务存在，镜像版本为：", find_app)
    } else {
        fmt.Println("服务不存在")
    }
    // port_url_basic := "https://api.alauda.cn/v1/services/hbykt/"

}
