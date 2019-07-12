package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
    "os"
)

func main() {
    client := &http.Client{}

    url := "https://api.alauda.cn/v1/services/hbykt?region_name=testing_clusers&project_name=default"
    request, err := http.NewRequest("GET", url, nil)
    if err != nil {
        log.Println(err)
        return
    }
    request.Header.Add("Authorization", "Token f6932eb5e800b143607e3ff124572a7e024bc2d2")
    // request.Header.Set("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    // q := request.URL.Query()
    // q.Add("api_key", "key_from_environment_or_flag")
    // q.Add("another_thing", "foo & bar")
    // request.URL.RawQuery = q.Encode()

    resp, err := client.Do(request)

    // fmt.Printf("%d", resp.StatusCode)

    defer resp.Body.Close()

    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        log.Println(err)
        return
    }

    type Service struct {
        ServiceName string `json:"service_name"`
        ImageName   string `json:"image_name"`
        ImageTag    string `json:"image_tag"`
    }

    type Result struct {
        Count   int
        Results []Service
    }

    fmt.Printf("body type: %T \n", body)
    serviceMap := make(map[string]string)
    result := &Result{}
    // 返回状态为1表示正常：result.Status == "1"
    json.Unmarshal(body, result) //解析json字符串
    for i := 0; i < len(result.Results); i++ {
        // fmt.Println(result.Results[i].ServiceName)
        // fmt.Println(result.Results[i].ImageName + ":" + result.Results[i].ImageTag)
        serviceMap[result.Results[i].ServiceName] = result.Results[i].ImageName + ":" + result.Results[i].ImageTag
    }
    serviceMapJson, _ := json.Marshal(serviceMap)
    if ioutil.WriteFile("list.json", []byte(serviceMapJson), os.ModeAppend) == nil {
        fmt.Println("文件写入成功")
    }
    find_app, ok := serviceMap["x-wechat"]
    if ok {
        fmt.Println("服务存在，镜像版本为：", find_app)
    } else {
        fmt.Println("服务不存在")
    }

}

/*
func WriteMaptoFile(m map[string]string, filePath string) error {
        f, err := os.Create(filePath)
        if err != nil {
                fmt.Printf("create map file error: %v\n", err)
                return err
        }
        defer f.Close()

        w := bufio.NewWriter(f)
        for k, v := range m {
                lineStr := fmt.Sprintf("%s^%s", k, v)
                fmt.Fprintln(w, lineStr)
        }
        return w.Flush()
}
*/
