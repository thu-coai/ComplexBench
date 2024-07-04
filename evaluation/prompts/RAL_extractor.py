EXTRACTION_PROMPT = """你是一个信息抽取专家。以下将会给你提供一个【输入指令】和对应的【模型回复】。此外，还会给你提供一个【评分问题】，设计该问题的目的是评测【模型回复】是否满足【输入指令】的某个要求。现在，你需要抽取出【模型回复】中，【评分问题】针对的评测对象。

例如，【模型回复】中包含两篇作文，若【评分问题】为“模型生成的第一篇作文是否不少于500字？”，则你只需要输出【模型回复】中的第一篇作文即可；
若【评分问题】为“模型生成的第二篇作文是否使用了生动的语言风格？”，则你只需要输出【模型回复】中的第二篇作文即可；
又例如，【评分问题】为“输出是否以“彭博社记者”作为输出的结尾？“，则你只需要输出【模型回复】的结尾**最后一句**。

**注意：你应该完全复制【模型回复】中连续的原文片段，严禁做任何修改、增添、删除、拼接，只能进行复制。同时强调，你的任务不是提取或构造出【模型回复】符合【评分问题】的部分，而是提取出【模型回复】中，【评分问题】针对的评测对象，即使其不符合【评分问题】要求。你不需要关注【评分问题】的具体要求是什么，更不需要评测【模型回复】是否满足【评分问题】要求。**
如果评分对象是整个【模型回复】，请你直接输出"all"。
如果评分对象在【模型回复】中不存在，请你直接输出"None"。

**注意**：通常而言，“开头”指的是文段的最开始一句话（第一个句号、感叹号、问号等为结尾标志），“结尾”指的是文段最末尾的一句话。

请先给出你对该任务的分析解释，然后输出你抽取的评测对象结果。

### 输出格式：
【解释】
XXX

【模型回复中评分问题的评测对象】
评分对象：XXX

你必须完全按照上述格式进行输出，禁止输出任何多余解释或多余标点。

### 例一

【输入指令】
分析下列艺术家及其代表作品：
1. 梵高——《星空》
2. 奥古斯特·罗丹——《思想者》
当该艺术家与作品匹配时，判断他属于画家还是雕塑家，如果是画家，生成一篇关于他作品的介绍，要求包含“文艺复兴时期”一词。如果是雕刻家，生成一篇关于这位艺术家的简介，要求在50字左右。
当该艺术家与作品不匹配时，判断他属于画家还是雕塑家，如果是画家，修正错误的作品名称，以“以下为修正内容”为开头进行输出。如果是雕塑家，则输出“请重新输入”。

【模型回复】
梵高——《星空》
梵高是荷兰后印象派画家，代表作品有《星空》、《向日葵》等。《星空》是他的成名作，展现了梵高独特的画风和色彩运用，是后印象派绘画的代表作之一。

2. 奥古斯特·罗丹——《思想者》
奥古斯特·罗丹是法国雕塑家，代表作品有《思想者》、《思想者》等。《思想者》是他的代表作之一，采用了立体主义风格，表现了人类思考和探索的精神内涵。

当该艺术家与作品匹配时：
梵高是画家。

当该艺术家与作品不匹配时：
需要重新输入作品名称。

【评分问题】
模型生成的关于奥古斯特·罗丹的简介文本是否在50字左右？


【解释】
该评分问题的评分对象是“关于奥古斯特·罗丹的简介文本”，所以需要直接输出【模型回复】中，奥古斯特·罗丹的简介文本对应部分。

【模型回复中评分问题的评测对象】
评分对象：奥古斯特·罗丹是法国雕塑家，代表作品有《思想者》、《思想者》等。《思想者》是他的代表作之一，采用了立体主义风格，表现了人类思考和探索的精神内涵。



### 例二

【输入指令】
“小明正在玩游戏，妈妈走过来说，‘你这样下去，将来一事无成。’小明回应说，‘我知道妈妈，我会注意时间管理。’”\n描述上面这段话的情景，要求分点明确，包括下列关键词中的1个：1. 时不我待 2. 杀鸡儆猴 3. 知错能改 4. 自知之明，字数在300字左右，以“完成。”作为结尾。

【模型回复】
首先，我们来看“时不我待”。在这个场景中，小明的母亲提醒他要珍惜时间，因为时间是无法等待的。她可能担心如果小明继续沉迷于游戏，他会错过很多学习和工作机会，最终一事无成。这种对时间的紧迫感反映了“时不我待”的关键词。\n\n接下来，我们看到“知错能改”。当小明的母亲警告他不要浪费时间时，小明承认了他的错误并表示会改进。他承诺会更加注意时间管理，这表明他已经意识到了自己的错误，并愿意采取措施来改正。这种承认错误并采取行动的态度正是“知错能改”的体现。\n\n总的来说，这段对话展示了小明在母亲的提醒下意识到时间的重要性，并表示会改变自己的行为。这个情景可以用“时不我待”、“知错能改”这两个关键词来描述。同时，我们也可以看到小明具有“自知之明”，能够认识到自己的问题并在母亲的提醒下采取行动。

【评分问题】
模型生成的描述结尾处是否为“完成。”？


【解释】
该评分问题的评分对象是【模型回复】的结尾部分。根据要求，需要提取出【模型回复】中结尾最后一句话。注意不应该输出“完成。”，它不是【模型回复】的结尾最后一句话。

【模型回复中评分问题的评测对象】
评分对象：同时，我们也可以看到小明具有“自知之明”，能够认识到自己的问题并在母亲的提醒下采取行动。



### 例三

【输入指令】
分析下列艺术家及其代表作品：梵高 -《蒙娜丽莎》
当该艺术家与作品匹配时，判断他属于画家还是雕塑家，如果是画家，生成一篇关于他作品的介绍，要求包含“文艺复兴时期”一词。如果是雕刻家，生成一篇关于这位艺术家的简介，要求在50字左右。
当该艺术家与作品不匹配时，判断他属于画家还是雕塑家，如果是画家，修正错误的作品名称，以“以下为修正内容”为开头进行输出。如果是雕塑家，则输出“请重新输入”。

【模型回复】
很抱歉，根据您提供的信息，无法确定艺术家梵高是否与《蒙娜丽莎》匹配。请您提供更多关于该艺术家的信息，以便我们进行更准确的判断。谢谢！

【评分问题】
模型对作品名称的修正是否以“以下为修正内容”为开头？


【解释】
该评分问题的评分对象是“模型对作品名称的修正”的开头部分，所以应该输出【模型回复】的开头第一句，即“很抱歉，根据您提供的信息，无法确定艺术家梵高是否与《蒙娜丽莎》匹配。”

【模型回复中评分问题的评测对象】
很抱歉，根据您提供的信息，无法确定艺术家梵高是否与《蒙娜丽莎》匹配。



### 例四

【输入指令】
福田区政务局副局长李东升将于 12月30日为成都七中初三的小朋友们介绍智慧政务的发展情况，激发孩子们的学习热情，请为他写一篇演讲稿。\n要求：\n1. 开头要感谢四川省委书记孙大强的支持，结尾要呼吁同学们努力。\n2. 全文不能出现”福田“两个字。\n3. 用一句英文的名言警句鼓励他们。\n最后为这篇演讲稿起一个不超过10个字的标题。

【模型回复】
### 演讲稿标题：智能未来的探索者\n\n尊敬的各位老师，亲爱的同学们，大家下午好！\n\n在这个美好的时刻，我有幸来到这里，和大家一起探讨智慧政务的未来。首先，请允许我代表区政务局，向长期以来关心和支持智慧政务发展的四川省委书记孙大强表示最诚挚的感谢！是他的卓见和推动，使我们得以在这条光明大道上稳步前行。\n\n智慧政务，简而言之，就是利用现代科技手段，如大数据、云计算等信息技术，来优化政府的服务和管理。想象一下，你是否有过等待许久才能办理某项政务服务的经历？智慧政务的目标，就是要让这样的等待成为历史，让政府服务像网购一样便捷，让数据多跑路，群众少跑腿。

【评分问题】
模型是否为这篇演讲稿起的标题是否不超过10个字？


【解释】
该评分问题是评测【模型回复】中，给演讲稿起的标题的字数，所以应该输出演讲稿的标题“智能未来的探索者”。注意不应该输出“演讲稿标题：”，这个仅仅是一些说明装饰文本，不是演讲稿真正的标题。

【模型回复中评分问题的评测对象】
评分对象：智能未来的探索者



### 例五

【输入指令】
请先告诉我贝多芬的第九交响曲中的合唱部分是基于哪位诗人的作品创作的？以“贝多芬的第九交响曲中的合唱部分是基于”开头回答。
然后对这首交响曲进行200字以内的简要评析，评析部分要分点作答，并且包含关键词"赏析内容如下："。

【模型回复】
贝多芬的第九交响曲中的合唱部分是基于德国诗人席勒的《欢乐颂》创作的。

简要评析：

1. 主题思想：贝多芬的第九交响曲以德国诗人席勒的《欢乐颂》为歌词，表达了人类对自由、平等和友爱的追求。这首交响曲被认为是人类精神的象征，展现了人类对美好未来的向往。

2. 音乐形式：贝多芬的第九交响曲采用了古典交响乐的形式，结构严谨、逻辑清晰。在音乐中，贝多芬巧妙地运用了和声、节奏和旋律等元素，展现了丰富的音乐风格和表现力。

【评分问题】
模型回复的评析部分是否包含关键词"赏析内容如下："？


【解释】
该评分问题是评测【模型回复】全文中是否包含“"赏析内容如下："”这个关键词，所以评测对象是【模型回复】整体，因此应该输出“all”。

【模型回复中评分问题的评测对象】
评分对象：all


### 例六

【输入指令】
邯郸市委网信办主办邯郸电信协办邀请各县（市、区）委网信办网络安全主管领导和科室人员2人。市直各有关单位网络安全处室负责同志及科室人员2人，参会地点中国电信邯郸分公司2楼大会议室，共计300余人参加，会议主题网络安全和参观电信展示厅，让各单位了解电信能力。

请你根据以上内容，写一篇不少于500字的信息稿，不可以使用分点格式，开头要求用“邀请函：邯郸市网络安全会议暨电信展示厅参观”来开头，结尾用“邯郸市委网信办”进行署名。

【模型回复】
邀请函：邯郸市网络安全会议暨电信展示厅参观

尊敬的各位领导、科室人员：

我们诚挚地邀请您参加由邯郸市委网信办主办，邯郸电信协办的邯郸市网络安全会议暨电信展示厅参观活动。此次会议旨在加强网络安全意识，提升网络安全防护能力，同时让您们更加了解电信能力。

一、会议时间：2022年10月15日（星期六）上午9:00-11:30
二、会议地点：中国电信邯郸分公司2楼大会议室
三、参会人员：各县（市、区）委网信办网络安全主管领导和科室人员2人，市直各有关单位网络安全处室负责同志及科室人员2人。

四、会议内容：
1. 网络安全主题演讲，邀请相关专家就当前网络安全形势、防护策略等方面进行深入讲解。
2. 参观电信展示厅，了解电信能力，感受高科技的魅力。

我们期待您的参加，共同提升网络安全防护水平，共创美好未来。

邯郸市委网信办
2022年10月10日

【评分问题】
输出是否以“邯郸市委网信办”结尾？


【解释】
该评分问题的评分对象是【模型回复】的结尾部分，所以应该输出【模型回复】的结尾最后一句，即“邯郸市委网信办\n2022年10月10日”。

【模型回复中评分问题的评测对象】
评分对象：邯郸市委网信办\n2022年10月10日


### 参考示例，提取如下【模型回复】中的【评分问题】针对的评测对象。
**再次强调：你应该完全复制【模型回复】中连续的原文片段，禁止做任何修改、增添、删除、拼接，只能进行复制。同时强调，你的任务不是提取或构造出【模型回复】符合【评分问题】的部分，而是提取出【模型回复】中，【评分问题】针对的评测对象，即使其不符合【评分问题】要求。**
**给出你的评测对象时，必须确保每一个字都是【模型回复】中真实存在的。

【输入指令】
{instruction}

【模型回复】
{response}

【评分问题】
{question}


【解释】"""


EXTRACTION_PROMPT_EACH = """你是一个信息抽取专家。以下将会给你提供一个【输入指令】和对应的【模型回复】。此外，还会给你提供一个【评分问题】，设计该问题的目的是评测【模型回复】是否满足【输入指令】的某个要求。现在，你需要抽取出【模型回复】中，【评分问题】针对的评测对象。

例如，【模型回复】中包含两篇作文，若【评分问题】为“模型生成的第一篇作文是否不少于500字？”，则你只需要输出【模型回复】中的第一篇作文即可；
若【评分问题】为“模型生成的第二篇作文是否使用了生动的语言风格？”，则你只需要输出【模型回复】中的第二篇作文即可；
又例如，【评分问题】为“输出是否使用了XX作为文章的结尾？“，则你只需要输出【模型回复】的结尾**最后一句**。

**注意：你应该完全复制【模型回复】中连续的原文片段，严禁做任何修改、增添、删除、拼接，只能进行复制。同时强调，你的任务不是提取或构造出【模型回复】符合【评分问题】的部分，而是提取出【模型回复】中，【评分问题】针对的评测对象，即使其不符合【评分问题】要求。你不需要关注【评分问题】的具体要求是什么，更不需要评测【模型回复】是否满足【评分问题】要求。**
已知评分对象在【模型回复】中存在多个，请你使用||将不同的评分对象分隔开。
如果评分对象在【模型回复】中不存在，请你直接输出"None"。

**注意**：通常而言，“开头”指的是文段的最开始一句话（第一个句号、感叹号、问号等为结尾标志），“结尾”指的是文段最末尾的一句话。

请先给出你对该任务的分析解释，然后输出你抽取的评测对象结果。

### 输出格式：
【解释】
XXX

【模型回复中评分问题的评测对象】
评分对象：XXX||YYY

你必须完全按照上述格式进行输出，禁止输出任何多余解释或多余标点。

### 例一

【输入指令开始】
在什么样的场景下会产生“怎么才能让头发看着蓬松很多”这样的用户痛点 ？请用简短的语句写一些日常的场景，每个场景用一句话概括，不允许除了句号外的其它标点。每句话以“场景1/场景2/场景X”开头。写8句话，每句话的字数不超过15个字。着重要求：以markdown表格的形式呈现，表格只需要一列“场景”。

【模型回复开始】
| 场景1 |\n| ---- |\n| 洗完头发后发现头发扁塌无精神。 |\n| 头发稀疏，看起来毫无蓬松感。 |\n| 想要在特殊场合展现蓬松发型。 |\n| 头发容易油腻，缺乏蓬松感。 |\n| 想要尝试新的蓬松发型。 |\n| 头发干燥无光泽，缺乏蓬松感。 |\n| 想要让头发看起来更加丰盈。 |\n| 想要让头发看起来更加有质感。 |

【评分问题开始】
模型生成的每个场景是否是以“场景X”开头？


【解释】
该评分问题的评分对象是【模型回复】中对每个场景的描述的开头，所以应该提取每个场景的描述的开头。

【模型回复中评分问题的评测对象】
评分对象：洗完头发后发现头发扁塌无精神。||头发稀疏，看起来毫无蓬松感。||想要在特殊场合展现蓬松发型。||头发容易油腻，缺乏蓬松感。||想要尝试新的蓬松发型。||头发干燥无光泽，缺乏蓬松感。||想要让头发看起来更加丰盈。||想要让头发看起来更加有质感。



### 例二

【输入指令开始】
为“松下剃须刀（松下小方盒）安萊精钢刀头，小巧机身便于携带”写一条带货短视频脚本。
以markdown表格输出，包括分镜序号、分镜内容、台词文本、运镜。
每个分镜的台词都要以疑问句开头，以感叹句结尾；每个分镜的台词不超过50字。

【模型回复开始】


| 分镜序号 | 分镜内容                               | 台词文本                                   | 运镜   |
| -------- | -------------------------------------- | ------------------------------------------ | ------ |
| 1        | 手持松下剃须刀，展示刀头和机身         | “这是松下剃须刀，安萊精钢刀头，看多小巧！” | 静态   |
| 2        | 拍摄手持剃须刀的人正在旅行或出门的场景 | “小巧的机身，便于携带，真是出门旅行的好选择！” | 跟随拍 |
| 3        | 展示剃须刀在使用时的效果               | “而且刮得干净利落，真是太方便了！”           | 特写   |
| 4        | 手持剃须刀，展示产品包装和价格           | “赶紧入手吧，这么好用的剃须刀，价格还这么实惠！” | 静态   |

【评分问题开始】
模型输出的每个分镜的台词是否以疑问句开头？


【解释】
该评分问题的评分对象是【模型回复】中每个分镜台词的开头，所以应该提取每个分镜台词的开头第一句话。

【模型回复中评分问题的评测对象】
评分对象：“这是松下剃须刀，安萊精钢刀头，看多小巧！”||“小巧的机身，便于携带，真是出门旅行的好选择！”||“小巧的机身，便于携带，真是出门旅行的好选择！”|| “而且刮得干净利落，真是太方便了！”||“赶紧入手吧，这么好用的剃须刀，价格还这么实惠！”



### 例三

【输入指令开始】
撰写一篇关于时尚新型法官的博客文章，要求字数在300字左右。文章中必须包含3个小标题，每个小标题前标有星号(*)。文章必须以导语开头，以结语结尾。在撰写时，请确保每个小标题下的内容都能够紧扣主题，提供有关时尚新型法官的有趣见解或信息。

【模型回复开始】
时尚新型法官：法庭上的时尚ICON

一、时尚与正义的完美结合
时尚与法律似乎是两个截然不同的领域，但是随着社会的不断发展，时尚新型法官正逐渐成为法庭上的新宠。这些法官不仅在法庭上展现出专业的法律素养，更以他们独特的时尚品味成为了法庭上的时尚ICON。他们的着装不仅展现了个人魅力，更传递出了一种自信和权威，让人们对法律和正义有了全新的认识。

二、时尚新型法官的着装风格
与传统的法官黑袍相比，时尚新型法官们的着装风格更加多样化和个性化。他们可能会选择搭配一件时尚的西装外套，或是配上一条别致的领带，甚至可能会在法庭上展现出一些时尚的配饰，如手表、眼镜等。这种与众不同的着装风格不仅让他们在法庭上脱颖而出，更让法庭变得更加生动有趣。

三、时尚新型法官的形象建设
时尚新型法官们的形象建设不仅仅停留在外表，更多的是通过自己的言行举止展现出对法律的尊重和对正义的追求。他们可能会在社交媒体上分享自己的时尚穿搭，与公众分享法律知识，甚至可能会参与一些公益活动，让更多的人了解法律，关注正义。通过这种形象建设，时尚新型法官们不仅仅是法庭上的执法者，更是社会上的时尚偶像和价值引领者。

结语：
时尚新型法官的出现，不仅让法庭变得更加有趣和生动，更让人们对法律和正义有了全新的认识。他们的时尚形象不仅仅是外在的展示，更是对法律和正义的一种内在追求。让我们一起期待更多时尚新型法官的出现，让法庭变得更加时尚与有趣。

【评分问题开始】
博客文章是否包含3个小标题？


【解释】
该评分问题的评分对象是【模型回复】中每个小标题，所以应该提取出其中的每个小标题。

【模型回复中评分问题的评测对象】
评分对象：一、时尚与正义的完美结合||二、时尚新型法官的着装风格||三、时尚新型法官的形象建设



### 例四

【输入指令开始】
帮我为一只黑白色的狗起三个名字，以json格式输出，只有一个字段“名字”，对应值为一个包含所有名字的list

【模型回复开始】
```json
{{
  "名字": ["奥利奥", "斑点", "墨墨"]
}}
```

【评分问题开始】
模型是否给出了三个名字？


【解释】
该评分问题的评分对象是【模型回复】中起的所有名字，所以应该提取出其中的所有名字。

【模型回复中评分问题的评测对象】
评分对象："奥利奥"||"斑点"||"墨墨"



### 例四

【输入指令开始】
想要推广一个农药科研新产品，可以采取哪五项推广措施？要求传播速度快、效果好、推广扎实。五项措施的内容请使用分号分隔。

【模型回复开始】
1. 网络营销与社交媒体推广：利用微博、微信、抖音等社交平台发布产品信息，利用短视频、直播等形式展示产品效果和使用方法；\n\n2. 与农业专业媒体合作：在农业杂志、专业网站、行业论坛等媒体上发布广告和专题报道，提高产品知名度；\n\n3. 参加农业展会和研讨会：在各类农业展览会上设立展位，进行现场演示和讲解，同时参与研讨会分享科研成果，与行业内人士建立联系；\n\n4. 建立试点示范基地：在不同地区建立试验示范点，邀请农户参观，亲眼见证产品效果，通过口碑传播增强信任度；\n\n5. 培训销售和技术服务团队：组织专业的销售和技术服务团队，对农户进行产品知识和使用技巧的培训，提供优质的售后服务，确保用户满意度。

【评分问题开始】
模型回复是否将五项措施的内容使用分号分隔？


【解释】
该评分问题的评分对象是【模型回复】中关于“想要推广一个农药科研新产品”的推广措施，所以应该将【模型回复】中提到的所有推广措施提取出来。

【模型回复中评分问题的评测对象】
评分对象：1. 网络营销与社交媒体推广：利用微博、微信、抖音等社交平台发布产品信息，利用短视频、直播等形式展示产品效果和使用方法；||2. 与农业专业媒体合作：在农业杂志、专业网站、行业论坛等媒体上发布广告和专题报道，提高产品知名度；||3. 参加农业展会和研讨会：在各类农业展览会上设立展位，进行现场演示和讲解，同时参与研讨会分享科研成果，与行业内人士建立联系；||4. 建立试点示范基地：在不同地区建立试验示范点，邀请农户参观，亲眼见证产品效果，通过口碑传播增强信任度；||5. 培训销售和技术服务团队：组织专业的销售和技术服务团队，对农户进行产品知识和使用技巧的培训，提供优质的售后服务，确保用户满意度。



### 参考示例，提取如下【模型回复】中的【评分问题】针对的评测对象。
**再次强调：你应该完全复制【模型回复】中连续的原文片段，禁止做任何修改、增添、删除、拼接，只能进行复制。同时强调，你的任务不是提取或构造出【模型回复】符合【评分问题】的部分，而是提取出【模型回复】中，【评分问题】针对的评测对象，即使其不符合【评分问题】要求。**
**给出你的评测对象时，必须确保每一个字都是【模型回复】中真实存在的。

【输入指令开始】
{instruction}

【模型回复开始】
{response}

【评分问题开始】
{question}


【解释】"""