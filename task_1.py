import libtmux
import os
import tqdm
import argparse


def start(session_name, num_users, base_dir='./'):
    """
    Запустить $num_users ноутбуков. У каждого рабочай директория $base_dir+$folder_num
    """
    cur_server = libtmux.Server()
    cur_session = cur_server.new_session(session_name)
    # cur_session = cur_server.find_where({ "session_name": session_name })

    for cur_user in tqdm.tqdm(range(num_users)):
        # Here I will start the enumeration from 1
        cur_window_name = "wind-" + str(cur_user + 1)
        cur_window = cur_session.new_window(attach=False, window_name=cur_window_name)
        pane = cur_window.split_window(attach=False)

        cur_dir = "user-" + str(cur_user + 1)
        cur_path = os.path.join(base_dir, cur_dir)

        try:
            os.mkdir(cur_path)
        except Exception:
            print("Can't create a directory: ", cur_dir)

        cur_ip = "127.0.0.1"
        cur_port = 8889 + int(cur_user)
        cur_token = "tok-" + str(cur_user + 1)

        command_line = "jupyter notebook --ip " + cur_ip + " --port " + str(cur_port) + \
                       " --no-browser --NotebookApp.token=" + cur_token + \
                       " --NotebookApp.notebook_dir=" + cur_path
        pane.send_keys(command_line, enter=True)


def stop(session_name, num):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    @:param num: номер окружения, кот. можно убить
    Предполагаем, что, как и у введенных выше номеров окружений, тут нумерация начинается с 1
    (если с 0, достаточно просто поменять в 4й строке num на (num+1)
    """
    cur_server = libtmux.Server()
    cur_session = cur_server.find_where({"session_name": session_name})
    all_windows = cur_session.list_windows()
    window_delete = all_windows[num]
    window_delete.kill_window()


def stop_all(session_name):
    """
    @:param session_name: Названия tmux-сессии, в которой запущены окружения
    """
    cur_server = libtmux.Server()
    cur_session = cur_server.find_where({"session_name": session_name})
    all_windows = cur_session.list_windows()
    for i in range(1, len(all_windows)):
        window = all_windows[i]
        window.kill_window()

    # There was not mentioned in the task either we want to kill a session directly or not, so:
    cur_server.kill_session(session_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", choices=["start", "stop", "stopall"],
                        required=True, help="start a session/stop a session/stop all sessions",
                        type=str)
    parser.add_argument("-s", "--session_name", required=False, default='session557',
                        help="enter the name of the session", type=str)
    parser.add_argument("-n", "--num_users", required=False, default=1,
                        help="enter the number of users", type=int)
    parser.add_argument("-k", "--num_win", required=False, default=0,
                        help="enter the number which you want to stop", type=int)
    parser.add_argument("-d", "--base_dir", required=False, default='./',
                        help="enter the base directory", type=str)

    args = parser.parse_args()

    if (args.command == "start"):
        start(args.session_name, args.num_users, args.base_dir)
    else:
        if (args.command == "stop"):
            if (args.num_win > 0):
                stop(args.session_name, args.num_win)
            else:
                print("num_win parameter must be positive: enumeration starts from 1")
        else:
            if (args.command == "stopall"):
                stop_all(args.session_name)
            else:
                print("The command is not correct!")


if __name__ == '__main__':
    main()
