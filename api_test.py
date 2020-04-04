import os

funcs = ['my_reps', 'state_reps']
for func in funcs:
    print('Checking {} function\n'.format(func))
    mock_dir = os.path.join(os.getcwd(), 'mocks', func)
    tests = os.listdir(mock_dir)

    for test in tests:
        print('Testing {}\n'.format(test))
        os.system('serverless invoke --function {} --path mocks/{}/{}'.format(func, func, test))
