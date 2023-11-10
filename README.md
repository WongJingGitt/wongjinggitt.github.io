## 一个基于React与Github Pages的博客项目  

----

### 项目介绍
这是一个简单的博客项目，基于React与Github Pages，使用GitHub Pages托管静态页面，使用GitHub Actions自动部署。  

我的初衷是：减少重复的配置，尽可能地“傻瓜式”操作。

我自认为现在基本实现了“傻瓜式”操作，项目会将blog目录下的目录层级与md文件映射到前端展示，除了首次部署时需要在`config/config.json`中更改个人信息。
后续只需要按照个人喜好将文件放在`blog`目录下，然后**运行main.py**提交到GitHub即可。

**blog目录不建议嵌套太深的层级，可能会有展示异常。**

也就是说**不管你怎么写，你只要写完把Markdown文件放在blog文件夹下面（可以用文件夹分类），然后运行main.py即可。**

博客界面UI使用的是字节跳动的[Semi Design](https://semi.design/zh-CN/)，个人挺喜欢这种风格。

效果预览：[https://wongjinggitt.github.io/](https://wongjinggitt.github.io/)

博客会将每个list语法块分割成卡片展示，所以可以在博客中用list语法写一些卡片式内容。

例如： 源语法
```markdown
- ### 序： 

    事请的起因是最近想用博客把日常工作中遇到的一些坑记录下来  

----

- ### 博客的选择：

    既然有了这个想法，就开始了解目前博客的主流方式
    > 直接用第三方提供的博客。如：CSDN、掘金、简书、知乎等  
    使用第三方工具自己搭建。如：Hexo等  
    
    我选择了自己搭建，主要是喜欢自己动手的快乐。  
    
    了解了下Hexo，感觉挺麻烦的，每次写新博客时还要使用CLI命令创建新文章。  
    我这个人比较 “懒” 。我想要的效果是：定义一个博客根目录，在根目录中用文件夹分类博客类型，然后把本地的层级映射到博客前端。  
    这样我在新增博客的时候直接Push到Github仓库就可以了。在新增的时候不用做额外的操作，只要新增文件夹或者文件就可以了。  
    
    **所以决定还是自己写一套逻辑，搭建一个简单的博客**  

----

- ### 技术方案：  

    既然决定自己写，就开始着手了。  
    首先，博客的后端，我选择用了[Github Pages](https://pages.github.com/)。Github Pages是一个静态文件托管服务器。用来做博客的后端再适合不过了。  
    前端我决定用 [React](https://react.dev/) + [Semi Design](https://semi.design/zh-CN/)  
    
```

实际展示时：

![](https://wongjinggitt.github.io/images/Readme/博客list语法示例.png)

并且list还可以嵌套使用，list内嵌套list，展示逻辑卡片内嵌套卡片。详细可以看我的博客。

----

### Tips

项目基本可以满足日常需求，但是有一个点：**仅支持原生Markdown语法，拓展语法需要以HTML标记语言书写。** 例如表格、字体颜色等等。

#### 拓展语法处理

```html
<!--表格-->
<table>
    <thead>
        <tr>
            <th>表格标题</th>
            <th>表格标题</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>表格内容</td>
            <td>表格内容</td>
        </tr>
    </tbody>
</table>

<!--字体颜色-->
<span style="color: red;">测试字体</span>
```

**表格在写的时候带上thead标签与tbody标签，不然无法区分表格标题与表格内容。**

#### 文档目录处理

项目会识别文档内**一级标题**（`h1`、`#`）一直到**六级标题**（`h6`、`######`），然后生成目录。  

文章内无需手动标记序号，目录组件会根据层级关系自动适配序号。

![](https://wongjinggitt.github.io/images/Readme/目录层级展示.png)

有兴趣的话可以把代码拉过去玩一玩。

----

### config配置

示例：

```json
{
    "username": "王英杰",
    "logo": "https://wongjinggitt.github.io/public/logo.svg",
    "email": "WongJingGit@163.com",
    "links": [
        {"title": "Github", "url": "https://github.com/WongJingGitt"},
        {"title": "Gitee", "url": "https://gitee.com/wangyingjie1003", "src": "https://gitee.com/static/images/logo-black.svg?t=158106664"}
    ]
}
```

![](https://wongjinggitt.github.io/images/Readme/config对应关系.png)

`logo`可以找免费的在线设计网站做一个，这种网站很多。

`links`接收多维数组作为配置项，每个配置项包含title、url、src(可选)三个属性。  

* title: 链接的标题
* url: 点击后跳转的链接
* src: 链接的图标，可选。可以从跳转网站的logo里提取出来，如果**填了将会使用src作为标题，并且不会展示title文案**，跳转交互保留。

----

### 目录说明

* `blog`: 博客存放目录
* `config`: 配置文件存放目录
* `images`: 图片存放目录
* `public`: 公共文件存放目录
* `static`: 博客前端静态文件存放目录
* `asset-manifest.json`: 前端静态资源映射文件
* `index.html`: 博客首页文件
* `main.py`: 主程序文件

----

### 安装

**部署之前记得更改`config.json`，删除仓库内的博客、图片、公共文件。**

```commandline
git clone https://github.com/WongJingGitt/wongjinggitt.github.io.git
cd wongjinggitt.github.io

// 删除博客
rmdir /s/q blog

// 创建blog文件夹
md blog

// 移除默认的远程仓库
git remote remove origin

// 添加远程仓库
git remote add origin <你的Github Pages仓库>
```

----

### 引用与依赖

- React: https://react.dev/
- Semi Design: https://semi.design/zh-CN
- React-Markdown: https://github.com/remarkjs/react-markdown
- React-Router-Dom: https://reactrouter.com/en/main