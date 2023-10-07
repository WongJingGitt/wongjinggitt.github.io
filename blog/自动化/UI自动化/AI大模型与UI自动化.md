- ### 序：

    先贴一下项目的链接：[Auto Flow AI](https://github.com/WongJingGitt/AutoFlowAI)

    事情的起因是换了新项目组需要做UI自动化，所以决定重新从零开始搭建一下UI自动化框架，温习一下以前的一些技术，顺带验证一下对于框架搭建一些新的想法。  
    
    在封装DOM元素捕获的方法时，想起了UI自动化最大的弊端：**太过于依赖DOM了。** 特别是在学习了一些前端知识之后，我愈发这样觉得。
    有时候一个组件可能样式外观没什么变化，但是背地里DOM层级与DOM选择器全都变了。<span style="color: rgb(198, 202, 205)">我当初就有过因为开发把导航栏的类名与DOM层级重构了，导致我所有的UI自动化用例都没跑起来。 = =</span>

    这也是在搭框架时，为什么要把DOM选择器与业务逻辑分离的重要原因之一。

    所以我就在想，**为什么人在操作界面的时候不需要DOM选择器？** <span style="color: rgb(198, 202, 205)">现在回过头想这个问题好幼稚 = =</span>

    怀这个问题，我去打开了一个网站，带着这个问题体验了下。

    我发现人在浏览网页、操作某个元素的时候，首先是通过外观识别一个页面组件，然后再脑海中把它归类到一个指定的分类中。
    
    例如，我在看某个库的文档的时候，首先第一步是观察整体的布局，然后识别导航栏在哪里。然后在导航栏里面找 `Docs` 字段。
    
    总结了一下，这里面主要有两个很重要的因素： 

    1. **视觉处理。**  
    2. **文字识别。** 

    仔细一想这两点其实就是`物体检测分类`与`OCR文字识别`，并且现在都有对应的解决方案了。

    那么也就是说：**其实机器也可以像人一样依靠视觉与文字来识别组件！**  
    
    所以就有了这个想法。

    有了这个想法之后，开始去了解相关的算法模型。最终选择了两个模型：`YOLO v8` 与 `Paddleocr`。  

- ### 模型介绍：
  
    - #### YOLO v8：
      
        [YOLO](https://pjreddie.com/) 全称是 `You Only Look Once` ，是由 `Joseph Chet Redmon` 开源的一个目标检测的模型。  
        但是这位老哥因为担心技术被滥用，特别是军事应用与隐私问题。所以在YOLO v3之后，他停止了YOLO的更新。  
  
        但是！虽然他停止开发，其他人仍然在更新这个项目。例如 [YOLO v6](https://github.com/meituan/YOLOv6)就是美团开源的，没错就是美团外卖那个美团。
        
        而[YOLO v8](https://github.com/ultralytics/ultralytics)则是由[ultralytics](https://ultralytics.com/)公司开源的，也是YOLO目前(2023/09)最新的版本。  
  
    - #### Paddleocr：
  
        [Paddleocr](https://github.com/PaddlePaddle/PaddleOCR)是百度PP飞桨开源的OCR文字识别框架，并且自带了预训练模型，基本可以做到开箱即用。 
  
        没啥好特别介绍的，因为是百度开源的，所以它的预训练模型对于中文的识别很好。个人实际体验中文的识别准确度在95%以上，很少出现识别错误。  
  
- ### 实操：

    实际使用中，Paddleocr是有预训练模型的，无需进行额外的训练。
    
    主要需要训练的是YOLO模型。  
    
    训练YOLO模型需要制作训练数据集，在制作时参考的了COCO数据集。

    - **手工制作数据集：**
        
        制作YOLO数据集时需要对图片中的目标进行标记，最常用的工具是`labelImg`。  

        我在最初的数据集制作时也是使用`labelImg`，但是标注了部分数据之后我发现这样**制作数据效率实在是太低了**：
  
        1. 打开项目地址，然后对各个页面进行截图保存。
        2. 用`labelImg`打开截图文件夹，手动圈选目标DOM。
        3. 圈选了目标DOM之后，需要手动输入对应的label。
      
        当一个图片中有10个需要标注的DOM时，需要重复步骤2、步骤3十次，而且这些标注DOM往往都会有大量重复的DOM组件。
        
        > 举一个很典型的例子：导航栏的标注，一个导航栏下面可能有几个甚至十几个item。而这些item可能只是文案不同，例如：订单管理、人员管理、权限管理 ......
  
        而在使用`labelImg`进行标注时，你必须老老实实把所有的item都进行圈选，并且绑定label。一张图片标注完可能需要好几分钟，效率极低。  

        在我标注了半小时数据，发现只标注了7张图片之后，我决心一定要寻找一种快速指标数据集的方法。  

    - **脚本制作数据集：**  
        
        有了这个想法之后，我大致整理了下思路。既然是对DOM的标注，首先就需要捕获DOM。  
  
        这里的捕获DOM与UI自动化中的捕获DOM不同，
        UI自动化需要捕获到某个指定的DOM，例如：登录按钮。  
        而数据集的制作不需要定位到详细的DOM，只需要捕获所有某个类型的DOM即可，例如：页面所有的按钮。  
        
        这里我首先想到的是，使用TagName来捕获所有的元素。就像这样：

        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/AI大模型与UI自动化/使用TagName捕获元素.png)

        但是实际使用中我发现，前端项目的组件往往会有很多不确定性。有一些组件TagName的位置，与这个组件在前端实际展示的位置是不相符的。  
        听起来可能有点抽象，这里面可能涉及到CSS组件设计相关的内容。总之据具体就像这样：

        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/AI大模型与UI自动化/TagName偏移.png)
        
        从这个例子可以看见，如果使用TagName，则拿到的位置其实是搜索框里面，那这样的标注肯定是无效的，因为它没有给模型输入整个搜索框，而是输入了搜索框的内部。  
        
        还有一些场景也有很大的问题，例如按钮可以使用`<button></button>`来写，还可以使用`<input type="button"/>`

        于是我便换了另一种方式：class。

        前端项目中UI组件设计，通常会遵循对应的规范。
        在设计通用组件时，往往会用class来绑定css样式，而这些class通常会遵循一定的命名规范。会把样式拆分成一个个class，然后按需绑定DOM。
        
        > 例如：最基础的按钮class可能是 `btn`，不同的按钮则会在`btn`之上增加对应的class。  
        因此禁用的按钮class可能是 `btn btn-disabled`。

        可以看这个例子中的关注与发消息按钮：

        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/AI大模型与UI自动化/class命名规律.png)        

        所以有了这个规律就好办了，在这个例子中，我只需要使用`h-f-btn`这个class就可以把这两按钮都捕获到。
        
        ![](https://wongjinggitt.github.io/images/自动化/UI自动化/AI大模型与UI自动化/class捕获元素.png)

        基于以上结论我整理出了一个粗略的逻辑：  
        
        1. 定义一个配置文件，用来记录需要识别的页面URL与DOM选择器。
        2. 使用`Playwright`打开项目的目标URL。
        3. 页面加载完之后，在页面遍历搜寻所有定义的DOM选择器。
        4. 在遍历选择器中：如果元素存在则得到的应该时一个列表，还需要循环一次DOM列表得到每一个DOM，然后获取DOM的在页面的坐标信息。
        5. 截图，然后将坐标信息转成YOLO标记。
        6. 保存截图与坐标文件。  
    
        有了逻辑接下来就是代码实现。具体已实现的完整代码在项目的[utils/label_generator.py](https://github.com/WongJingGitt/AutoFlowAI/blob/master/utils/label_generator.py)中。  
        这里就只贴一点核心代码讲解一下。  
        
        ```python
        for url in urls:
            self.__page.goto(url)
            self.__page.wait_for_timeout(REDIRECT_TIME)

            visible, hidden = self._element_visibility_classify(selector_strs=self._selectors)

            # 首先搜一遍初始的位置，然后把hidden(当前处于可视窗口外)中还没有进行捕获的元素逐一地进行滚动到可视窗口内进行捕获，然后更新hidden直到hidden为空。
            while True:
                data_name = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}__{int(random.random() * 10000000)}"
                yolo_datas = [f'{index} {self._element_position_for_yolo(selector)}' for index, selector in visible]

                # 爬B站首页时出现空yolo_datas陷入死循环的情况，优化这类场景
                if not yolo_datas:
                    print(url, '搜寻完毕')
                    print()
                    break

                with open(path.join(self._label_path, f'{data_name}.txt'), 'w') as fw:
                    yolo_datas = '\n'.join(yolo_datas)
                    self.__page.screenshot(path=path.join(self._image_path, f'{data_name}.png'))
                    self._filelist.append(data_name)
                    fw.write(yolo_datas)
                    fw.close()

                print(data_name, '已写入')
                print()

                if not hidden:
                    print(url, '搜寻完毕')
                    print()
                    break
                hidden[0][1].scroll_into_view_if_needed()

                visible, hidden = self._element_visibility_classify(selector_strs=hidden)
        ```  
        
        这里面有涉及到了一个`element_visibility_classify`函数不得不讲一下，也是我在编写这个脚本过程中踩过的一个坑。  
        
        在实际页面中，所有的DOM都会被加载到DOM树。但是当前的窗口可能会放不下，所以就会触发滚动条。
        也就是说：**某个DOM虽然在DOM树层面是可见的，但是在初始的界面其实是不可见的。可能需要向右或者向下滚动才能展示在页面。**  
        
        这个时候就需要滚动页面，然后再截图并且捕获元素打YOLO标签。  

        ```python
        def _element_visibility_classify(self, selector_strs: list[str or Locator or ElementHandle]) -> tuple[
            list[Locator or ElementHandle], list[Locator or ElementHandle]]:
            """
            根据元素在窗口内的可见性，将DOM元素分类为窗口内可见、窗口内不可见或隐藏。
            :param selector_strs: 要分类的选择器列表。
            :return: 包含可见和隐藏元素的元组。
            """
            visible = []
            hidden = []

            for index, selector_str in enumerate(selector_strs):
                # 判断是否是初次调用，初次调用时selector_str的是字符串。
                if isinstance(selector_str, str):
                    selector_str = self._convert_selector(selector_str)
                    selectors = self.__page.query_selector_all(selector_str)
                    # 优化处理，确保selectors是可迭代对象
                    selectors = selectors if not selectors else []
                else:
                    # 优化处理，当不是初次调用时传入的格式时 (label索引, 元素对象)。如果不用数组包裹后续遍历会遍历元组导致_, selector = result分解失败
                    selectors = [selector_str]

                for selector in selectors:
                    # 如果是初次调用，把label索引和元素对象用元组绑定
                    result = selector if not isinstance(selector_str, str) else (index, selector)
                    _, selector = result
                    try:
                        if self._visible_check(selector):
                            visible.append(result)
                        elif not self._visible_check(selector):
                            hidden.append(result)
                    except TypeError:
                        pass
            return visible, hidden
        ```  
        
        这里的核心逻辑其实就是：**传入一个DOM元素的列表，然后遍历每一个元素。判断元素是当前窗口可见还是不可见（需要滚动）。** 
        然后把可见和不可见的元素分开放入两个列表，最后返回。  
        
        在调用这个函数时：
        
        1. 初始的元素列表会被分为可见与不可见两种。
        2. 然后在可见的元素捕获完毕之后，把页面滚动到不可见的列表第一个元素，让其出现在窗口中。
        3. 把不可见的元素再重新作为一个新的列表传入到`_element_visibility_classify`中。因为此时页面已经滚动了一次，`hidden`列表中的部分元素以处于可见状态。需要重新划分一次。  
        4. 再继续捕获可见的元素。此时`hidden`列表的长度已经变小。  
        5. 循环`步骤2`、`步骤3`、`步骤4`，直到输出的`hidden`列表长度为0。  
      
        这样就完美解决了这个问题。  
    
- ### 心得总结：
    
    整个项目编写来下其实也踩了挺多的坑的，很多小的优化点这里就不拿出来讲了。  
    这个项目对于机器配置还是有一定的要求的，尤其是训练模型时。  

    在实际的业务使用中，推理一个页面普通的办公电脑还是需要挺久时间的，主要的时间是耗费在ocr识别上。
    
    所以我认为大部分时候这个项目适合做为一个兜底操作存在，当常规手段捕获DOM失败时可以用这个方式去捕获DOM。  
    
    或者，在DOM组件颗粒划分的足够细的情况下，不需要借助ocr来分辨不同的子组件。
    > 例如：前面讲到的两个按钮，我在制作训练数据集时，统一使用了`h-f-btn`来捕获它，那么训练出来的模型最小只能识别到按钮这个粒度。
    这个时候在推理它只能识别出所有的按钮，比如它会把登录按钮、注册按钮一起识别成按钮，没办法做到识别哪一个是登录、哪一个是注册。所以这时候需要借助ocr来识别按钮中的文字，从而识别不同的组件。
    但是如果训练数据集得粒度标注得足够细，比如每一个组件、每一个类型按钮在制作训练数据集时都做了单独的标注，这个时候模型就可以识别出足够粒度的按钮。
    
    这个时候在实际使用时就不需要使用ocr，可以节省大部分时间，我认为这个时候这个项目是可以作为主要框架来使用的。

    还有一个点，如果是训练了的DOM，YOLO无法识别，那可能是发生了样式上的错误，这个是常规的UI自动化很难做到的。  
    
    其实我最终想实现的效果是最大限度的减少代码编写，降低UI自动化的门槛，最终可以直接通过自然语言来进行UI自动化测试。  
    在编写用例的时候，只需要在配置文件中用白话文来描述用例的步骤，通过自然语言模型来处理文本然后生成对应的UI自动化测试代码并且执行。  
    
    或者也可以，直接输入功能测试用例，然后根据功能测试用例来生成UI自动化代码进行测试。

    这样的话理论上来说或许某些不涉及到UI新增或者改动的新需求也可以直接使用这个框架进行测试。  

    总之，继续加油吧！