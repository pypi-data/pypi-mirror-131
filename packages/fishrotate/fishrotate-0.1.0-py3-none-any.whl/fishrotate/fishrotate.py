'''
作者: 小鱼
公众号: 鱼香ROS
QQ交流群: 2642868461
描述: file content
'''
import sys
import argparse
import rclpy
try:
    import transforms3d as tfs
except:
    print("请先安装transforms3d..")

from fishrotate.RoateAnimation import RoateAnimation


def main(args=None):
    # if args is None:
        # args = sys.argv[1:]
    
    parse = argparse.ArgumentParser(description='fishrotate:基于ROS2的坐标旋转动画工具\r\n使用样例:fishrotate rxyz base rotate 0.0 0.0 0.0 45.0 60.0 90.0')

    rotate_types = ''
    for rotate_type in tfs.euler._AXES2TUPLE.keys():
        rotate_types += f'{rotate_type},'

    parse.add_argument("rotate_order",default="rxyz",type=str,help=f'旋转顺序：{rotate_types[:-1]},默认:rxyz')
    parse.add_argument("origin",default="base",type=str,help=f'原坐标系名字，默认:base')
    parse.add_argument("rotate",default="rotate",type=str,help=f'旋转的坐标系名字,默认:rotate')
    parse.add_argument("x",default="0.0",type=float,help=f'rotate沿origin的X轴平移,默认:0.0')
    parse.add_argument("y",default="0.0",type=float,help=f'rotate沿origin的Y轴平移,默认:0.0')
    parse.add_argument("z",default="0.0",type=float,help=f'rotate沿origin的Z轴平移,默认:0.0')


    parse.add_argument("r1",default="0.0",type=float,help=f'绕第1个转轴的旋转,默认:45.0')
    parse.add_argument("r2",default="0.0",type=float,help=f'绕第2个转轴的旋转,默认:60.0')
    parse.add_argument("r3",default="0.0",type=float,help=f'绕第3个转轴的旋转,默认:90.0')


    parse.add_argument("speed",default="10.0",type=float,help=f'旋转速度，度/秒,默认:10.0')

    args = parse.parse_args()
    print(f"发布{args.origin}到{args.rotate}的动画，平移:{args.x},{args.y},{args.z},旋转:{args.rotate_order}:{args.r1},{args.r2},{args.r3} 速度:{args.speed}")

    rclpy.init()
    rotate = RoateAnimation(div=args.speed/100.0)
    rotate.add_transform(args.origin,
                args.rotate,
                [args.x,args.y,args.z],
                [args.r1,args.r2,args.r3],
                order=args.rotate_order
                )
    rclpy.spin(rotate)


