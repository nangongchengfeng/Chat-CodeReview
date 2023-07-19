# Chat-CodeReview(Gitlab)

>  ChatGPT automates code review for GitLab's code. 

 Translation Versions: [ENGLISH](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.md) | [中文简体](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-CN.md) | [中文繁體](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.zh-TW.md) | [한국어](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ko.md) | [日本語](https://github.com/nangongchengfeng/Chat-CodeReview/blob/main/README.ja.md) 

## Features

 **ChatGPT integrates with GitLab to achieve automated code auditing and provide efficient, intelligent code review solutions for software development teams**

> 1. Automatic Trigger and Timely Response: Utilizing GitLab's Webhook functionality, the system automatically triggers events such as code submissions, merge requests, and tag creations. Upon receiving new code submissions, the system promptly responds by initiating the auditing process without manual intervention.
> 2. Integration with GitLab API Interface: Through integration with GitLab's API interface, the solution allows for easy extension and expansion of functionalities. This integration enhances flexibility in interacting with GitLab, accommodating a wide range of customized auditing requirements.
> 3. Comprehensive Automated Auditing: ChatGPT performs automatic code audits on GitLab's code, encompassing three types of code submissions: push (commit), merge (merge request), and tag (tag creation). Whether it involves new code submissions or code merges, the system automatically examines and provides audit comments.
> 4. Retrying Mechanism: To address potential network anomalies or other issues, the system incorporates a retrying mechanism. In the event of a failed request due to network problems, the system automatically retries to ensure the reliability and stability of the auditing process.

## Principles of auditing

![1689647943933](images/1689647943933.png)

 **steps：** 

> 1. GitLab's Webhook Event Push: GitLab can be configured with Webhooks to trigger notifications when events such as code submissions or merge requests occur. Upon new code submissions or merge requests, GitLab sends a POST request to a pre-defined URL, containing relevant event data.
> 2. Parsing Diff Content and Sending to ChatGPT: After receiving the Webhook event, GitLab parses the diff content, representing the differences between the new code and existing code. Subsequently, these differences are sent to ChatGPT's API endpoint, enabling ChatGPT to comprehend the code changes.
> 3. ChatGPT Processing and Returning Results: ChatGPT, a powerful natural language processing model, is capable of understanding and processing natural language text. When ChatGPT receives the diff content, it analyzes and comprehends the code changes, providing an assessment and feedback on potential issues, vulnerabilities, or optimization suggestions. ChatGPT returns the processed results to the triggering GitLab instance.
> 4. Displaying ChatGPT's Processed Results as Comments: GitLab receives the processed results from ChatGPT and adds them as comments to the corresponding code submissions or merge requests. Consequently, code contributors and other team members can review ChatGPT's audit results and make appropriate improvements or fixes based on the recommendations.

 By integrating GitLab's code auditing with ChatGPT, automatic code quality checks and reviews can be accomplished, thereby assisting teams in identifying potential issues, vulnerabilities, or opportunities for improvement. (The above is for reference only.) 



## prompt

###  Experienced leadership 

```python
    messages = [
        {"role": "system",
         "content": "You are a seasoned programming expert, tasked with reviewing code changes in GitLab commits. The code modifications will be provided as Git diff strings, and you will assign a score to each change in the format of "Score: actual score," with a scoring range of 0 to 100. Your feedback should be concise yet rigorous, highlighting the identified issues using precise language and a stern tone. If necessary, you may provide the revised content directly. Your feedback must adhere to the strict conventions of Markdown format."
         },
        {"role": "user",
         "content": f"Please review the following code changes: {content}",
         },
    ]
```

###  Proud and spirited young woman 

To review, refer to the following role statement:

```python
{
    "role": "system",
    "content": "You are a prodigious young girl, proficient in the realm of programming. With a touch of haughtiness and pride, your role entails scrutinizing the code modifications made by your predecessors. You elegantly and playfully employ the Markdown format to point out any issues, injecting the vibrancy and buoyancy of youth. Feel free to embellish your feedback with captivating emojis, adding charm and liveliness to your messages."
}
```

 

## environment variable

> -  gitlab_server_url :  URL address of the Gitlab server
> -  gitlab_private_token :  A private access token (private token) for accessing the Gitlab API 
> -  openai_api_key :  The key used to access OpenAI's API



## Gitlab WebHook

GitLab's Webhook is an event notification mechanism that allows you to configure a URL address within GitLab. When specific events occur, GitLab sends an HTTP request to that URL, transmitting the relevant event data to your application. This enables your application to perform custom operations or responses based on the received event data.

Webhooks can be utilized to monitor and respond to various events within GitLab, such as code commits, merge requests, tag creation, branch operations, and more. By leveraging Webhooks, you can implement a wide range of automation tasks, integrations, and Continuous Integration/Continuous Deployment (CI/CD) workflows.

 The following are the key features and uses of GitLab's Webhook: 

> 1. Event Trigger: When you configure and enable a Webhook in GitLab, it automatically triggers when specific events occur, such as code commits or merge requests.
> 2. HTTP Requests: Once an event is triggered, GitLab sends an HTTP request to the URL you have configured in advance. This request contains the relevant event data, typically in JSON format. The most common method used is the POST request.
> 3. Custom Operations: By writing a script or service that receives Webhook requests, you can parse and handle the received event data, allowing you to execute custom operations. Examples include automated builds, automated testing, and automated deployment.
> 4. Integration with other services: Webhooks enable GitLab to integrate with other services and tools. For instance, you can automatically sync code with a Continuous Integration (CI) platform, send notifications to team members, or update a task tracking system.
> 5. Configurability: GitLab's Webhook provides extensive configuration options. You can choose the types of events to monitor, set trigger conditions, and define the content and format of the request.



![1689651530556](images/1689651530556.png)

![1689651554862](images/1689651554862.png)

------

### Test data (push)

**Request URL:** POST http://192.168.96.19:5000/git/webhook 200

**Trigger:** Push Hook

**Elapsed time:** 0.01 sec

**Request time:** 刚刚

------

##### Request headers:

```
Content-Type: application/jsonX-Gitlab-Event: Push HookX-Gitlab-Token: asdhiqbryuwfqodwgeayrgfbsifbd
```

##### Request body:

```
{
  "object_kind": "push",
  "event_name": "push",
  "before": "95790bf891e76fee5e1747ab589903a6a1f80f22",
  "after": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "ref": "refs/heads/master",
  "checkout_sha": "da1560886d4f094c3e6c9ef40349f7d38b5d27d7",
  "message": "Hello World",
  "user_id": 4,
  "user_name": "John Smith",
  "user_email": "john@example.com",
  "user_avatar": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
  "project_id": 15,
  "project": {
    "id": 15,
    "name": "gitlab",
    "description": "",
    "web_url": "http://test.example.com/gitlab/gitlab",
    "avatar_url": "https://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=8://s.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?s=80",
    "git_ssh_url": "git@test.example.com:gitlab/gitlab.git",
    "git_http_url": "http://test.example.com/gitlab/gitlab.git",
    "namespace": "gitlab",
    "visibility_level": 0,
    "path_with_namespace": "gitlab/gitlab",
    "default_branch": "master"
  },
  "commits": [
    {
      "id": "c5feabde2d8cd023215af4d2ceeb7a64839fc428",
      "message": "Add simple search to projects in public area",
      "timestamp": "2013-05-13T18:18:08+00:00",
      "url": "https://test.example.com/gitlab/gitlab/-/commit/c5feabde2d8cd023215af4d2ceeb7a64839fc428",
      "author": {
        "name": "Test User",
        "email": "test@example.com"
      }
    }
  ],
  "total_commits_count": 1,
  "push_options": {
    "ci": {
      "skip": true
    }
  }
}
```

##### Response headers:

```
Server: Werkzeug/2.3.6 Python/3.8.0Date: Tue, 18 Jul 2023 03:39:51 GMTContent-Type: application/jsonContent-Length: 26Connection: close
```

##### Response body:

```
{
  "status": "success"
}
```



## install and run

### 1、download code

```python
git clone https://github.com/nangongchengfeng/chat-review.git
```

### 2、install dependencies

![1689663745702](images/1689663745702.png)

```python
python deal_package.py
```

### 3、update configuration

**config/config.py**

```python

"""
这个文件是用来从apollo配置中心获取配置的，
如果没有apollo配置中心，可以直接在这里配置
"""

WEBHOOK_VERIFY_TOKEN = "asdhiqbryuwfqodwgeayrgfbsifbd"
gitlab_server_url = gitlab_server_url
gitlab_private_token = gitlab_private_token
openai_api_key = openai_api_key

```

### 4、run app.py 

```python
简单
nohup python3 app.py & 
```

### 5、Gitlab  Webhook

```python
http://192.168.96.19:5000/git/webhook 
The IP address of the running machine can be changed, and the domain name can also be changed.
http://gitlab.ownit.top/git/webhook 
```



![1689651530556](images/1689651530556.png)



## question

### diff processing

![1689661104194](images/1689661104194.png)

#### Method 1 (succinct)

1、Pass all the contents of the acquired diff to chatgpt for processing (including adding lines and deleting lines)

 **Advantages**: Convenient and fast. 

 **Disadvantages**: If the content is too long, it may cause issues with ChatGPT's processing, resulting in partial code and potentially incoherent logic 



#### Method 2 (recommended)

2、The processing of obtaining the diff content involves removing deleted lines and the "+" symbol.

**Advantages**: It is convenient, fast, and saves a considerable amount of space.

**Disadvantages**: If the content is too lengthy, it may lead to ChatGPT's processing failure, resulting in only a partial code and fragmented logic.

```python
def filter_diff_content(diff_content):
    filtered_content = re.sub(r'(^-.*\n)|(^@@.*\n)', '', diff_content, flags=re.MULTILINE)
    processed_code = '\n'.join([line[1:] if line.startswith('+') else line for line in filtered_content.split('\n')])
    return processed_code
```

![1689661743140](images/1689661743140.png)



#### Method 3 (Complicated) Not joint debugging, the code has been overwritten

3、 Process the content of the diff, remove deleted lines and the '+' symbol, retrieve the modified original file, and use JavaParser for parsing. Obtain the corresponding code blocks and upload them for review. 

 **Advantages**: Saves space, provides completed methods, and slightly improves the logic. 

 **Disadvantages**: Very cumbersome and tedious, only supports Java. 

```json
[{
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'SettlementDetailController'
}, {
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'queryRecord'
}, {
	'code': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	'name': 'populateBatchItemVO'
}]
```



## Demo

![1689663598079](images/1689663598079.png)



## contribute

Thanks to [ anc95  小安大佬](https://github.com/anc95) for the support and inspiration of the project
https://github.com/anc95/ChatGPT-CodeReview.git

 ![Avatar](images/13167934.jpg) 



