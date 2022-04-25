def gen_test_name(pc, msg):
    return f"{pc['start'].strftime('%Y%m%d')}_{pc['end'].strftime('%Y%m%d')}_{pc['period']}_{msg}"
