#CoordinateClient 160223
    Aimed at:
        Make some data analyze with picture coordinate
    Environment:
        Windows 8.1 - 64
        Python 2.7.10 (with Image installed)
    Attention:
        Variables:
            size: produce a x-y size coordinate
            splitline: build splitline on specific points of both axis
            blank: blank space for data point to expand
            padding: padding of two data point, blank is not in padding
        Functions:
            create_img: create image
            inside_xy_change: change user's input xy to actual position on picture
            get_point: return state of point specificed by user's input xy
            add_point: add data (blank->filled, filled->expand to blank) based on input xy
            create_splitline: create splitline
            resize_img: resize the image
            save: save the image
        Tips:
            Image will automatically resize when blank is not enough for expanditure
            xy will not change with the actual size, so don't worry

    目标：
        使用图片坐标轴直观的展示数据分布、趋势情况
    环境：
        Windows 8.1 - 64
        Python 2.7.10 （使用Image插件）
    注意事项：
        变量解释：
            size: 生成x * y的坐标轴
            splitline: x, y轴特定值上建立辅助线
            blank: 每个数据节点边上空出的扩张区间
            padding: 两个数据之间（数据包括了其blank）的间隔，即blank不在padding内
        方法解释：
            create_img: 创建图片
            inside_xy_change: 将用户输入的x, y值转化为图片上实际的像素点坐标
            get_point: 获取用户输入的x, y值的点目前的状态（颜色）
            add_point: 在用户输入的x, y 值的点增加一个数据（无颜色->有颜色，有颜色->扩张）
            create_splitline: 添加辅助线
            resize_img: 重置图片大小
            save: 保存图片
        特殊内容：
            当blank不能容纳下数据节点的数据时图片会自动扩张
            使用时不必在意图片的实际大小，任何大小时的xy值含义相同

