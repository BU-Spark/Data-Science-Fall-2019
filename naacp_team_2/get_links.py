import os
import waybackpack


if __name__ == '__main__':
    os.system('waybackpack --from-date 201401 --to-date 201812 --list www.bostonglobe.com >bostonglobe.txt')
    os.system('waybackpack --from-date 201401 --to-date 201812 --list www.wgbh.org >wgbh.txt')
    os.system('waybackpack --from-date 201401 --to-date 201812 --list www.wbur.org >wbur.txt')