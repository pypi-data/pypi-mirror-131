import cmath
import re


# 每行组件数据model
class ComponentModel(object):
    # 组件名
    name = ''
    # 版本号
    version = ''
    # git地址
    git = ''
    # 分支名
    branch = ''
    # configurations
    configurations = ''
    # other
    other = ''

    def __init__(self, name='', version='', git='', branch='', configurations='', other=''):
        self.name = name
        self.version = version
        self.git = git
        self.branch = branch
        self.configurations = configurations
        self.other = other

    def logInfo(self):
        print("name:", self.name)
        print("version:", self.version)
        print("git:", self.git)
        print("branch:", self.branch)
        print("configurations:", self.configurations)


def isVersion(version):
    rule = "\.{2,10}"
    rule2 = "^\d+(\.\d+){0,10}$"
    res = re.search(rule, version)
    if (res == None):
        result = re.search(rule2, version)
        if (result):
            return True
        else:
            return False
    else:
        return False


# 解析podfile中的pod每一行到ComponentModel对象
def parseForPodLine(line):
    pod_strip_line_segs = line.replace(" ", "").split(',')
    cm = ComponentModel()
    for segment in pod_strip_line_segs:
        if 'pod\'' in segment:
            cm.name = segment.replace('pod\'', '  pod \'')
        elif ':git' in segment:
            cm.git = segment
        elif ':branch' in segment:
            cm.branch = segment
        elif ':configurations' in segment:
            cm.configurations = segment
        elif isVersion(segment.replace('\'', '')):
            cm.version = segment
        else:
            cm.other = segment
    return cm


# 解析podfile中每一行
def parseForPodfile(podfile_lines):
    # 是否到target行
    targetBegin = False
    # 是否target下对应的end出来
    outTarget = True
    ret = []
    for podfile_line in podfile_lines:
        podfile_lstrip_line = podfile_line.lstrip()
        # 这些开头的字段，左边如果有空格就全去掉
        if podfile_lstrip_line.startswith("install! ") or \
                podfile_lstrip_line.startswith("source ") or \
                podfile_lstrip_line.startswith("target ") or \
                podfile_lstrip_line.startswith("pod ") or \
                podfile_lstrip_line.startswith("platform "):
            pass
        elif not podfile_lstrip_line:
            continue
        else:
            podfile_lstrip_line = podfile_line

        if podfile_lstrip_line.startswith("target "):
            targetBegin = True
            outTarget = False
            targetArr = []
        elif podfile_lstrip_line.startswith("end"):
            if targetBegin:
                targetBegin = False
                targetArr.append(podfile_lstrip_line + '\n')
        elif not podfile_lstrip_line:  # 空行处理
            continue

        # 已经进入target体，开始解析target内容
        if targetBegin:
            if podfile_lstrip_line.startswith("pod "):
                cm = parseForPodLine(podfile_lstrip_line)
                contained = False
                for pod in targetArr:
                    if isinstance(pod, ComponentModel) and pod.name == cm.name:
                        contained = True
                        break
                if not contained:
                    targetArr.append(cm)
            else:
                targetArr.append(podfile_lstrip_line)
        elif not outTarget:
            outTarget = True
            ret.append(targetArr)
        else:
            ret.append(podfile_lstrip_line)
    return ret


# 检查podfile是否符合规范，不支持嵌套target
def checkForPodfile(podfile_lines):
    targetBegin = 0
    for line in podfile_lines:
        podfile_lstrip_line = line.lstrip()
        if podfile_lstrip_line.startswith("target "):
            targetBegin += 1
            if targetBegin >= 2:
                return False
        if podfile_lstrip_line.startswith("end"):
            targetBegin -= 1
    return True


# 将单个组件的版本号更新到podfile
def update_component_to_model(name, version, podfile_model):
    for target in podfile_model:
        if isinstance(target, list):
            for component in target:
                if isinstance(component, ComponentModel):
                    if 'pod \'%s\'' % name == component.name.lstrip():
                        component.version = version
                        break


# 将最终结果重写到podfile中
def rewrite_to_podfile(podfile_path, podfile_model):
    contents = ''
    # model 转为字符串
    for target in podfile_model:
        if isinstance(target, list):
            for component in target:
                if isinstance(component, ComponentModel):
                    # 有版本号直接用版本号，没版本号则原样拼出
                    if component.version:
                        pod = "%s, %s \n" % (component.name, component.version)
                    else:
                        pod = component.name
                        if component.git:
                            pod += ", %s" % component.git
                        if component.branch:
                            pod += ", %s" % component.branch
                        if component.configurations:
                            pod += ", %s" % component.configurations
                        if component.other:
                            pod += ", %s" % component.other
                    contents += pod
                else:
                    contents += component
        else:
            contents += target
    with open(podfile_path, 'w+') as podfile:
        podfile.write(contents)


# 更新podfile中的组件指向新版本号
# 传过来的参数是：组件名:版本号
def update_component_with_newversion(podfile_path, components):
    print('获取到参数为：', podfile_path, components)
    # 读取podfile文件，翻译为对象
    with open(podfile_path, 'r') as podfile:
        _podfile_lines = podfile.readlines()
        if not checkForPodfile(_podfile_lines):
            print("podfile 不符合要求（不能target嵌套）")
            exit(-90)
        podfile_model = parseForPodfile(_podfile_lines)
    # 把传过来的组件更新到对象中
    for component in components:
        _componentSeg = component.split(':')
        if len(_componentSeg) == 2:
            name = _componentSeg[0]
            version = _componentSeg[1]
            update_component_to_model(name, "'%s'" % version, podfile_model)
        else:
            raise Exception("传过来的组件格式不对 %s" % component)

    # 把新的内容写入到podfile中
    rewrite_to_podfile(podfile_path, podfile_model)


if __name__ == '__main__':
    f_podfile = '/Users/lch/Desktop/Podfile'
    # f_podfile = '/Users/lch/Documents/ziroom/proj/Podfile'
    update_component_with_newversion(f_podfile, ['aaa:1.0', 'bbb:2.0'])
