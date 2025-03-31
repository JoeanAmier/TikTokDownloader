import axios from "axios";
import * as qs from 'qs'


export const HttpServerAddress = "https://wwww.baidu.com"

const instance = axios.create({
  baseURL:HttpServerAddress
})


instance.interceptors.request.use(
  config => {
    config.headers.Authorization =  localStorage.getItem("token")
    return config
  },
  error => {
    console.log(error)
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  response => {
    if (response.status === 200) {
      return Promise.resolve(response);
    } else {
      return Promise.reject(response);
    }
  },
  error => {
    console.log(error.response)
    if(error.response.status){
      switch(error.response.status) {

      }
      return Promise.reject(error.response);
    }
  }
)

export async function HttpGet(url, params){
  return new Promise((resolve, reject) => {
    instance.get(url + "?" + qs.stringify(params))
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.data)
      })
  })
}

export async function HttpPost(url, params){
  return new Promise((resolve, reject) => {
    instance.post(url,{data:params})
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.data)
      })
  })
}

export async function HttpPostForm(url, params){
  return new Promise((resolve, reject) => {
    instance.postForm(url,{data:params})
      .then(response => {
        resolve(response.data)
      })
      .catch(error => {
        reject(error.data)
      })
  })
}


export async function HttpPut(){}
export async function HttpDelete(){}
export async function DownloadFile(){}