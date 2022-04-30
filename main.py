import argparse
import json5
from reserve import reserve

parser = argparse.ArgumentParser()

# Add a command line argument for a config file
parser.add_argument("-c", "--config", help="所用的配置文件", default="config.jsonc")
parser.add_argument("-n", "--name", help="你的姓名")
parser.add_argument("-p", "--phone", help="你的手机号")

parser.add_argument("--time", help="预约时间", default="19:30")
parser.add_argument("--barber", help="理发师", default="都可以")
parser.add_argument("--mode", help="预约项目", default="理发")
parser.add_argument("--max", help="可以容忍的预约人数", default=2)

DEFAULT_TIMES = ["9:30", "10:00", "10:30", "11:00", "11:30", "12:00",
                 "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",
                 "18:00", "18:30", "19:00", "19:30"]

name = ""
phone_number = ""
times = []
max = 0
barber = "都行"
mode = "理发"

config_object = {}

args = parser.parse_args()

# If the user specifies a config file, load it
if args.config:
    with open(args.config, "r") as f:
        config_object = json5.load(f)

# 确定预约者姓名
if "name" in config_object.keys():
    name = config_object["name"]
elif args.name:
    name = args.name
else:
    name = input("请输入你的姓名：")

# 确认预约者电话号码
if "phone" in config_object.keys():
    phone_number = config_object["phone"]
elif args.phone:
    phone_number = args.phone
else:
    phone_number = input("请输入你的电话号码：")

# 确认预约时间优先级表
if "times" in config_object.keys():
    for time in config_object["times"]:
        if time in DEFAULT_TIMES:
            times.append(time)
        else:
            print("配置文件|无效的预约时间：" + time)
if args.time:
    for time in args.time.split(","):
        if time in DEFAULT_TIMES:
            times.append(time)
        else:
            print("命令参数|无效的预约时间：" + time)
times = times + [time for time in DEFAULT_TIMES if time not in times]

# 确认可以容忍的预约数
if "max" in config_object.keys():
    max = config_object["max"]
else:
    max = args.max

# 确认理发师
if "barber" in config_object.keys():
    barber = config_object["barber"]
else:
    barber = args.barber

# 确认预约项目
if "mode" in config_object.keys():
    mode = config_object["mode"]
else:
    mode = args.mode

if __name__ == "__main__":
    is_success, time = reserve(name, phone_number, times, max, barber, mode)
    if is_success:
        print("预约成功，时间{}".format(time))
    # print(name, phone_number, times, max, barber, mode)
