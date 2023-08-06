#!/bin/bash
## config param
dataId="com.xiaomai.cloud.acm:tam.yaml"
group="DEFAULT_GROUP"
namespace="118f1761-5aab-4f0b-a50c-42bb930fcba0"
accessKey="LTAICJxzmaULYj9c"
secretKey="IuyLYoZsUgyXtpVUBHuY7kxD7Jaszk"
endpoint="acm.aliyun.com"
## config param end
## get serverIp from address server
serverIp=`curl $endpoint:8080/diamond-server/diamond -s | awk '{a[NR]=$0}END{srand();i=int(rand()*NR+1);print a[i]}'`
## config sign
timestamp=$[$(date +%s)*1000]
signStr=$namespace+$group+$timestamp
echo -n $signStr
signContent=`echo -n $signStr | openssl dgst -hmac $secretKey -sha1 -binary | base64`
echo -n $signContent
## request to get a config
curl -H "Spas-AccessKey:"$accessKey -H "Timestamp:"$timestamp -H "Spas-Signature:"$signContent "http://"$serverIp":8848/nacos/v1/cs/configs?dataId="$dataId"&group="$group"&tenant="$namespace
