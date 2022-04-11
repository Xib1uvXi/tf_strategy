from xbacktesting.ru_bt import new_default_xbt
from vnpy.trader.optimize import OptimizationSetting


if __name__ == '__main__':
    xbt = new_default_xbt(1)

    target = "total_return"
    optimization_setting = OptimizationSetting()
    optimization_setting.set_target(target)

    optimization_setting.add_parameter("b_ma_window", 3, 66, 1)

    retults = xbt.run_bf_optimization(optimization_setting)
    print(f"best result\t 参数：{retults[0][0]}, 结果：{target}: {retults[0][1]}")