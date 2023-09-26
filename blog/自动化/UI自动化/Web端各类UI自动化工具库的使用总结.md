- ### 序  

  市面上的UI自动化工具其实挺多的，但是各有所长。
  这篇博客主要是对我使用过的**Web端UI自动化工具**进行**分析对比**，并给出我个人的**评价和建议**。  

- ### 语言  

    Web端UI自动化使用的主流语言主要有：`Python`、`Node.JS/JavaScript`、`Java`、`Ruby`等。  
    
    在这些语言中，使用人群比较多的是：`Python`、`Node.JS`。  

    根据我个人的经验，在国内使用`Python`来进行UI自动化测试的比较多，并且自动化的执行与编写都是由测试人员来进行。  

    而`Node.JS`通常是前端开发人员在进行`单元测试`时使用。<span style="color: rgb(198, 202, 205)" >PS: 但是据我了解很少有前端开发会进行单元测试 = =</span>  

    > **个人观点：**  
        由于UI自动化主要是对前端进行测试，而作为前端三件套的`Javascript`无疑是更加适合UI自动化的。  
        并且`Node.JS`具有**事件驱动**和**非阻塞IO**的特性，所以能够高效地处理大量的并发请求。  
        而UI自动化会涉及到大量的IO操作，例如：`打开浏览器`、`加载网页`、`点击元素`、`输入文本`、`截图`等。    
        如果使用**同步编程**的话，每个IO操作都会阻塞后面的代码，导致程序运行**缓慢**和**低效**。  
        而如果使用**异步编程**的话，每个IO操作都会在后台进行，不影响后面的代码执行，从而**提高**程序的**速度**和**效率**。
    
    但是**从团队的角度来说，`Python`无疑是更佳的选择**，尤其是团队成员具有一定的`Python`语言基础时，这种优势更加明显。  
    
    `Python`语法简单，在我看来很多基础语法根本就是英文直译，所以学习成本相对较低。  
    
    并且`Python`的社区相对比较庞大，说直白点，在使用`Python`进行UI自动化时，你能踩到的坑大部分都会有前人踩过，并且会在互联网留下对应的解决办法。  

    - **总结：**
        
        <table border="1">
            <thead>
                <tr>
                    <th>比较点</th>
                    <th>Python</th>
                    <th>Node.js</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>广泛的库支持</td>
                    <td>✔</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>易学易用</td>
                    <td>✔</td>
                    <td>⨉</td>
                </tr>
                <tr>
                    <td>跨平台性</td>
                    <td>✔</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>性能</td>
                    <td>⨉</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>线程限制</td>
                    <td>⨉</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>异步非阻塞</td>
                    <td>⨉</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>速度快</td>
                    <td>⨉</td>
                    <td>✔</td>
                </tr>
                <tr>
                    <td>学习曲线</td>
                    <td>低</td>
                    <td>高</td>
                </tr>
                <tr>
                    <td>CPU密集型任务</td>
                    <td>⨉</td>
                    <td>⨉</td>
                </tr>
            </tbody>
        </table>
    
    以上是我对于编程语言选择的一些分析，具体还是结合团队的实际情况来选择。总结成一句话就是：  
    如果想要**更优的运行性能**，使用**Node.JS**，  
    如果想要**更低的门槛**，使用**Python**。  

- ### 工具库  

    UI自动化的工具库的发展，我个人认为可以分为两个阶段：**早期**与**现代**。  
    
    它们之间主要体现在使用的底层技术不同。  

    #### 特点：    

    - 早期的UI自动化工具，以`Selenium`、`Robot Framework`为例：  
    
        > 它们无法直接与浏览器进行通讯，往往要借助第三方驱动如：WebDriver。也因为这样，它们的运行效率要低于新一代工具，并且使用门槛要高于新一代工具。<span style="color: rgb(198, 202, 205)">PS：我真的见过有人在用Selenium时，WebDriver驱动装了一下午都没装好的。</span>
        
        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/Web端各类UI自动化工具库的使用总结/Selenium原理.png)    

    - 新一代UI自动化工具，以`Playwright`、`Cypress`为例：  
  
        > 新一代的UI自动化工具往往是借助浏览器的特性，直接与浏览器进行通讯，不需要借助第三方驱动。  
        例如：  
            1. `Playwright`：是基于浏览器自身的`DevTools`协议来与浏览器通讯，它提供了一种更直接的方法来控制浏览器行为，包括页面导航、DOM操作等。  
            2. `Cypress`：`Cypress`是基于`Electron`构建的，`Electron`是一款用于制作跨平台应用的工具，它的底层是基于`Chromium`浏览器。而`Cypress`利用了这个特性，把测试代码运行在主进程之外，与Electron的渲染进程共享上下文。这意味着Cypress的测试脚本可以直接访问应用程序的DOM

        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/Web端各类UI自动化工具库的使用总结/Playwright原理.png)    
        
        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/Web端各类UI自动化工具库的使用总结/Cypress原理.png)
        
    <table>
        <thead>
            <tr>
                <th>工具名称</th>
                <th>所属时期</th> 
                <th>与浏览器的通讯方式</th>
                <th>运行效率(相对)</th>
                <th>支持的语言</th>
                <th>总结</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Selenium</td>
                <td>早期</td>
                <td>通过WebDriver进行通讯</td>
                <td>相对较低</td>
                <td>多语言支持，包括Python和JavaScript</td>
                <td>流行的早期UI自动化工具，但运行效率较低，配置复杂。</td>
            </tr>
            <tr>
                <td>Robot Framework</td>
                <td>早期</td>
                <td>通过WebDriver进行通讯</td>
                <td>相对较低</td>
                <td>支持多种语言，包括Python和JavaScript</td>
                <td>具有可扩展性的自动化框架，但需要第三方驱动。</td>
            </tr>
            <tr>
                <td>Playwright</td>
                <td>新一代</td>
                <td>直接使用浏览器的DevTools协议通讯</td>
                <td>相对高</td>
                <td>支持多种语言，包括Python和JavaScript</td>
                <td>新一代工具，高效且提供了丰富的API。</td>
            </tr>
            <tr>
                <td>Cypress</td>
                <td>新一代</td>
                <td>基于Electron构建，直接访问应用程序的DOM</td>
                <td>相对高</td>
                <td>主要支持JavaScript</td>
                <td>适用于现代Web应用测试，与应用程序深度集成。</td>
            </tr>
        </tbody>
    </table>

    #### 详细优缺点：

    - **早期的UI自动化：**
        
        提起UI自动化相信很多人第一反应是`Selenium`，这从侧面证实了`Selenium`的影响力。  
        与`Selenium`同时期的自动化框架还有`Robot Framework`。  

        `Selenium`和`Robot Framework`是两种早期流行的Web UI自动化测试框架，它们有各自的优缺点，并且底层的实现原理都不同。  

        `Selenium`更适合需要高度**定制化**和**灵活性**的测试场景。  
        `Robot Framework`更适合需要**快速开发**和维护的测试场景。
        两者之间也可以进行集成，利用`Selenium`提供的库作为`Robot Framework`的扩展库，实现Web UI自动化测试。  
        
        - **Selenium：**
      
            Selenium最早是由Jason Huggins在2004年开发的一个JavaScript程序，可以自动控制浏览器的操作，这个程序就是Selenium Core的雏形。  
            
            > 它的底层是通过浏览器驱动`WebDriver`来控制浏览器，模拟用户的操作，比如点击、输入、滚动等，同时也可以获取页面元素的属性和内容。  
            通过`WebDriver`它可以与多种浏览器进行交互，包括`Chrome`、`Firefox`、`IE`等。  
            `WebDriver`定义了一系列标准命令和协议的接口，它可以让不同语言编写的客户端代码与不同浏览器提供的服务器端代码进行通信。     
    
            具有以下的优点：  
            
            1. 支持多种浏览器和操作系统  
            2. 支持多种编程语言编写测试脚本
            3. 支持分布式测试和并行测试  
            4. 支持录制和回放的功能
            5. 支持与其他测试框架和工具集成  
        
            但`Selenium`同时也拥有以下缺点：
            
            1. 没有内置的图像比较功能，需要第三方软件\库
            2. 没有自带的报告功能，需要第三方插件
            3. 需要安装和配置浏览器驱动
            4. 需要处理一些浏览器和网页的兼容性问题
        
        - **Robot Framework：**  

            `Robot Framework`是芬兰人Pekka Laukkanen，在2006年提交了一篇题为“Data-Driven and Keyword-Driven Test Automation Frameworks”的硕士论文，阐述了他的设计思想。  
          
            同年，`Robot Framework`有了第一个版本，使用`Python`语言开发，支持`HTML`和`TSV`格式的测试数据。  
    
            > Robot Framework底层是通过SeleniumLibrary库来和浏览器进行通讯。  
            SeleniumLibrary是一个基于Selenium WebDriver的扩展库，它提供了一系列的关键字来操作浏览器，例如：打开浏览器、输入文本、点击元素等。SeleniumLibrary可以支持多种浏览器，比如Chrome、Firefox、IE等，只要安装了相应的浏览器驱动。
            
            具有以下的优点：
                
            1. 语法简单，使用表格格式编写测试数据  
            2. 支持关键字驱动和数据驱动的测试方法
            3. 支持用户自定义关键字和变量  
            4. 支持控制结构和本地化  
            5. 提供了HTML格式的报告和日志  
            6. 提供了多种扩展库来支持不同的平台和应用  
            7. 提供了远程测试执行接口和事件监听接口  
          
            同时也有以下缺点：
            
            1. 速度较慢，不适合大量数据的测试  
            2. 需要安装和配置Python环境和相关库
            3. 需要学习和掌握不同库的关键字用法
            4. 需要处理一些库之间的兼容性问题

    - **新一代的UI自动化：**

        新一代的自动化工具我使用过的有：`Playwright`、`Puppeteer`、`Cypress`。  
        
        简单讲一下我的体验感受：
        
        - **Playwright：**
          
            > 微软开源的UI自动化工具。能够控制FireFox、Webkit、Chrome。可以使用`NodeJS`与`Python`进行开发，但我多使用Python。
            底层是基于浏览器的DevTools协议。有两套API，分别是异步与同步。但是由于Python的语言特性，我多使用同步API。
            与Selenium一样，它需要结合第三方测试框架来进行用例编写、测试报告输出。  
            
            优点：
            
            1. 多浏览器、多语言，对于准备过渡到这个工具的用户非常友好。
            2. 基于浏览器的DevTools协议，运行速度相对较快。
            3. 拥有同步与异步两套API（Python），降低了使用门槛。
            4. 安装简单，直接使用pip安装软件包即可，无需进行额外操作。

            缺点：
            
            1. 学习曲线较陡峭，相对较新，使用者可能需要一些时间来学习和适应其API和工作原理。
            2. 社区支持相对较少。

        - **Puppeteer：**
            
            > 谷歌开源的UI自动化工具，默认的浏览器是Chromium，但是可以通过内置的API，结合ChromeLauncher库控制Chrome浏览器。如果有debug链接的话理论上所有chromium内核的浏览器都支持控制，本人实测Edge、QQ浏览器都可以控制。  
            Puppeteer是基于NodeJS的一个库，有Python开发者编写了第三方库Pyppeteer，但貌似好久没有更新了。
            我多使用NodeJS，它与Playwright一样也没有内置测试框架，也许需要结合第三方测试工具来编写用例、输出测试报告。
            
            优点：
            
            1. 安装简单，无需进行额外操作。
            2. 网页截图支持图片格式和PDF格式。
            3. 可以抓取SPA（单页应用程序）并生成预渲染内容（即“SSR”（服务器端渲染））。
            4. 可以捕获网站的时间线轨迹以帮助诊断性能问题。
            
            缺点：
            
            1. 仅支持NodeJS。
            2. 社区支持相对较少（对比Selenium）。
            3. 学习成本高，不懂NodeJS的测试人员需要先学习NodeJS。

        - **Cypress：**
        
            > [Cypress](https://www.cypress.io/)在国内使用的人应该挺少的，但个人认为这是我目前为止使用过最省心的UI自动化测试工具了。
            它内置了`Mocha`测试框架，并且内置直观的测试报告。但它的缺点也挺明显的，可拓展性不强。类似于Android与iOS的区别。
            如果你图省心的话可以使用Cypress
          
            优点：
            
            1. 提供了简洁的API和直观的界面，使得编写和运行测试变得非常容易。
            2. 可以在代码更改时自动重新加载页面，提供了快速的反馈，加快了测试的开发速度。
            3. 提供了强大的调试功能，可以在测试运行过程中检查页面元素和网络请求等，帮助开发者更好地定位问题。
            4. 内置测试报告与测试框架，无需结合第三方框架使用。
            5. 全局隐式等待，无需编写额外代码，每一个步骤之间都会自动等待
            6. 可以直接对前端框架的单个组件进行测试，支持对Vue、React、Angular、Svelte编写的单个组件进行测试。
          
            缺点：
            
            1. 自由度低，可拓展性低。
    
    下面是整体对比：

    <table border="1">
        <thead>
            <tr>
                <th>工具名称</th>
                <th>优点</th>
                <th>缺点</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Selenium</td>
                <td>支持多种浏览器和操作系统，多语言支持，支持分布式测试和并行测试，可以录制和回放测试用例，可以与其他测试框架和工具集成</td>
                <td>没有内置的图像比较功能，没有自带的测试报告功能，需要安装和配置浏览器驱动，需要处理一些浏览器和网页的兼容性问题</td>
            </tr>
            <tr>
                <td>Robot Framework</td>
                <td>语法简单，支持关键字驱动和数据驱动的测试方法，支持用户自定义关键字和变量，提供HTML格式的报告和日志，提供多种扩展库来支持不同的平台和应用，提供远程测试执行接口和事件监听接口</td>
                <td>运行速度较慢，需要安装和配置Python环境和相关库，需要学习和掌握不同库的关键字用法，需要处理一些库之间的兼容性问题</td>
            </tr>
            <tr>
                <td>Playwright</td>
                <td>支持多浏览器，多语言，适用于广泛的用例，基于浏览器的DevTools协议，运行速度相对较快，提供了同步和异步两套API，降低了使用门槛，安装简单，直接使用pip或npm安装软件包即可</td>
                <td>学习曲线较陡峭，相对较新，可能需要时间适应其API和工作原理，社区支持相对较少</td>
            </tr>
            <tr>
                <td>Puppeteer</td>
                <td>安装简单，无需额外配置，支持网页截图和PDF生成，可捕获SPA并生成预渲染内容，提供时间线轨迹捕获，有助于性能问题诊断</td>
                <td>仅支持Node.js，社区支持相对较少，学习成本较高，需要了解Node.js</td>
            </tr>
            <tr>
                <td>Cypress</td>
                <td>提供简洁的API和直观的界面，便于编写和运行测试，自动重新加载页面，提供快速反馈，强大的调试功能，帮助定位问题，内置测试报告和测试框架，省去了第三方集成，全局隐式等待，无需额外代码</td>
                <td>自由度较低，可拓展性不强，仅支持Chrome浏览器</td>
            </tr>
        </tbody>
    </table>

