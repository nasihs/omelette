import os
import subprocess
""" import time

start = time.clock() """

def image_to_string(img, cleanup=True, plus=''):
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    subprocess.check_output('tesseract ' + img + ' ' +
                            img + ' ' + plus, shell=True)  # 生成同名txt文件
    text = ''
    with open(img + '.txt', 'r') as f:
        text = f.read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text

print(image_to_string('./pics/cap24_dil.png', True, '-psm 7'))

""" elapsed = (time.clock() - start)
print("Time used:",elapsed) """