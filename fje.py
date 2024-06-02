import argparse
import json

# 组合模式：定义抽象组件
class Component:
    # 组件的初始化方法
    def __init__(self, name, father=None, children=None, is_last=0):
        self.name = name  # 名称
        self.father = father  # 父节点
        self.children = children  # 子节点列表
        self.is_last = is_last  # 是否为兄弟节点中的最后一个节点

# 定义叶子节点组件，继承自 Component
class Leaf(Component):
    def __init__(self, name, father, is_none=0):
        super().__init__(name, father=father)
        self.is_None = is_none  # 是否为空的叶子节点

# 定义树枝节点组件，继承自 Component
class Node(Component):
    def __init__(self, name, father=None, is_last=0):
        super().__init__(name, father=father, children=[], is_last=is_last)

    def add(self, child):
        self.children.append(child)  # 添加子节点

class Icon:
    def __init__(self, icon_map):
        self.Node_icon = icon_map['Node']
        self.Leaf_icon = icon_map['Leaf']

    def get_node_icon(self):
        return self.Node_icon

    def get_leaf_icon(self):
        return self.Leaf_icon

# 工厂方法：定义了输出的风格，只需添加新的工厂，即可添加新的风格
class Style:
    subclasses = {}
    def __init__(self, icon):
        self.icon = icon

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses[cls.__name__.lower()] = cls

    def show_as_father(self, node):
        pass  # 作为父节点时的输出

    def show_as_leaf(self, node):
        pass  # 作为叶子节点时的输出

    def show(self, node):
        pass  # 输出节点

# 树形风格，继承自 Style
class Tree(Style):
    def __init__(self, icon):
        super().__init__(icon)

    # 作为父节点时输出缩进
    def show_as_father(self, node):
        if node.father is not None:  # 不输出根节点
            self.show_as_father(node.father)  # 递归向上寻找父节点，每个父节点输出对应的缩进
            if node.is_last:
                print('   ', end='')
            else:
                print('|  ', end='')

    # 作为叶子节点时的输出
    def show_as_leaf(self, node):
        if not node.is_None:
            print(': ' + node.name)
        else:
            print('')

    # 主入口，输出节点的树形结构
    def show(self, node):
        if node.father is not None:  # 不输出根节点
            self.show_as_father(node.father)  # 先让所有父节点决定缩进
            if type(node.children[0]) is Node:  # 判断输出的icon样式
                icon = self.icon.get_node_icon()
            else:
                icon = self.icon.get_leaf_icon()
            if node.is_last:  # 如果该节点是兄弟节点中的最后一个节点，则说明后续没有兄弟节点
                print('└─' + icon + node.name, end='')
            else:  # 否则说明后续还有兄弟节点
                print('├─' + icon + node.name, end='')
            if icon == self.icon.get_node_icon():  # 如果子节点不是叶子节点，则直接换行，否则则让叶子节点负责换行
                print('')
        # 遍历所有子节点并输出
        for child in node.children:
            # 根据子节点类型选择输出的函数
            if type(child) is Node:
                self.show(child)
            else:
                self.show_as_leaf(child)

# 矩形风格，继承自 Style
class Rectangle(Style):
    def __init__(self, icon, line_width=45):
        super().__init__(icon)
        self.line_width = line_width  # 总行宽
        self.width = 0  # 当前宽度
        self.begin_mark = '┌'  # 每个节点的前缀标记
        self.end_mark = '┐'  # 每一行的结束标记
        self.bottom_turn = '└'  # 底部转折标记

    # 检查该节点是否是整棵树的最后一个叶子节点或其父亲
    def is_all_last(self, node):
        if node is None:
            return True
        if not node.is_last:
            return False
        return self.is_all_last(node.father)

    # 作为父节点时输出缩进
    def show_as_father(self, node):
        if node.father is not None:  # 不输出根节点
            self.show_as_father(node.father)  # 递归向上寻找父节点，每个父节点输出对应的缩进
            self.width += 3  # 记录当前行宽
            if self.begin_mark == '┴':  # 如果前缀标记是┴，则说明当前在输出整个表格的最后一行
                print(self.bottom_turn + '--', end='')  # 输出缩进
                if self.bottom_turn == '└':  # 如果是最后一行，则在输出完左下角的└后，后续该对应位置的符号就要变成┴
                    self.bottom_turn = '┴'
            else:
                print('|  ', end='')

    # 作为叶子节点时的输出
    def show_as_leaf(self, node):
        # 如果叶子节点非空则输出其内容，否则什么都不输出。最后补全该行
        if not node.is_None:
            print(': ' + node.name + '-' * (self.line_width - self.width - len(node.name) - 3) + self.end_mark)
        else:
            print('-' * (self.line_width - self.width - 1) + self.end_mark)
        if self.end_mark == '┐':  # 如果结束标记是┐，则说明第一行输出完成，将符号更改为┤交给后续输出使用
            self.end_mark = '┤'

    # 输出节点的矩形结构
    def show(self, node):
        if node.father is not None:  # 不输出根节点
            self.width = 0  # 每一行输出前先重置当前行宽
            self.show_as_father(node.father)  # 先让父节点输出缩进
            if type(node.children[0]) is Node:  # 判断输出的icon样式
                icon = self.icon.get_node_icon()
            else:
                icon = self.icon.get_leaf_icon()
            print(self.begin_mark + '─' + icon + node.name, end='')  # 输出节点名字和开始标记
            self.width += 3 + len(node.name)  # 记录行宽的变化
            if self.begin_mark == '┌':  # 如果前缀标记为┌，则说明当前为第一行，将符号更改为├交给后续输出使用
                self.begin_mark = '├'
            if icon == self.icon.get_node_icon():  # 如果子节点不是叶子节点，则说明该行输出结束，直接补全该行
                print('-' * (self.line_width - self.width - 1) + self.end_mark)
                if self.end_mark == '┐':  # 如果结束标记为┌，则说明第一行输出完成，将符号更改为┤交给后续输出使用
                    self.end_mark = '┤'
        # 遍历所有子节点并输出
        for child in node.children:
            #  如果该节点是整棵树的最后一个叶子节点的父亲，则说明到了最后一行，修改前缀标记和结束标记
            if type(child) is Node and type(child.children[0]) is Leaf and self.is_all_last(child):
                self.begin_mark = '┴'
                self.end_mark = '┘'
            # 根据子节点类型选择输出的函数
            if type(child) is Node:
                self.show(child)
            else:
                self.show_as_leaf(child)

# 建造者模式：用于构建组件树
class ComponentBuilder:
    def build_component(self, data, father):
        pass

# 具体建造者：根据 JSON 数据构建组件树
class JSONComponentBuilder(ComponentBuilder):
    def build_component(self, data, father=None, is_last=0):
        # 如果data是字典，说明不是叶子节点
        if isinstance(data, dict):
            # 遍历键值对，将当前data建立为节点，并创建其子节点
            for name, child in data.items():
                node = Node(name=name, father=father, is_last=is_last)
                # 如果子数据为字典，说明不是叶子节点
                if isinstance(child, dict):
                    for index, (key, value) in enumerate(child.items()):
                        node.add(self.build_component(data={key: value}, father=node, is_last=index == len(child.items()) - 1))
                else:  # 如果子数据不是字典，说明是叶子节点
                    node.add(self.build_component(data=child, father=node))
                return node
        # 如果data不是字典，则根据其是否非空来建立叶子节点
        elif data is None:
            return Leaf(name='', father=father, is_none=1)
        else:
            return Leaf(name=str(data), father=father)

# 指挥者
class Director:
    def __init__(self, builder):
        self.builder = builder

    def show_json(self, data, style):
        component = self.builder.build_component({'root': data}, is_last=1)
        style.show(component)

class FunnyJsonExplorer:
    def __init__(self, json_path, config_path, style_name, icon_name):
        # 读取JSON文件
        with open(json_path, "r") as file:
            self.data = json.load(file)

        # 读取配置文件
        with open(config_path, "r", encoding='utf-8') as file:
            self.config = json.load(file)

        # 在配置文件中取出图标
        icon = Icon(self.config[icon_name])
        # 使用反射机制根据命令行参数实例化相应的风格类
        self.style = Style.subclasses[style_name](icon)

        # 创建指挥者
        builder = JSONComponentBuilder()
        self.director = Director(builder)

    def show(self):
        self.director.show_json(self.data, self.style)


# 使用示例
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='处理JSON文件并以指定样式显示')

    parser.add_argument('-f', '--file', type=str, default='test.json', help='JSON文件路径')
    parser.add_argument('-s', '--style', type=str, default='tree', help='显示风格')  # choices=['tree', 'rectangle']
    parser.add_argument('-i', '--icon', type=str, default='icon1', help='图标家族')  # choices=['icon1', 'icon2']
    args = parser.parse_args()

    FJE = FunnyJsonExplorer(args.file, 'config.json', args.style, args.icon)
    FJE.show()

