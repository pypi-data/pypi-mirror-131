# -*- coding: utf-8 -*-

import argparse
import os
import sys
import requests

if __name__ == "__main__":
    import my_util as my_util
else:
    import hhdpy.my_util as my_util

USAGE = """
--orgs google-developer-training
python /Users/hhd/project/hhdpy/hhdpy/and_clone_2_install.py --orgs google-developer-training
"""

NEW_GRADLE_DISTRIBUTION_URL_LIST = [
    "distributionUrl=https\://services.gradle.org/distributions/gradle-4.8-bin.zip",
    "distributionUrl=https\://services.gradle.org/distributions/gradle-7.0.2-bin.zip",
]


# curl   -H "Accept: application/vnd.github.v3+json"   https://api.github.com/orgs/google-developer-training/repos

def run(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--orgs")
    parser.add_argument('--install', action='store_true')
    options = parser.parse_args(args)
    print(f"orgs:{options.orgs}")
    print(f"install:{options.install}")

    home_dir = my_util.subprocess_check_output(f"echo $HOME", ".")
    pwd = my_util.subprocess_check_output(f"pwd", ".")

    res = requests.get(f"https://api.github.com/orgs/{options.orgs}/repos", headers={"Accept": "application/json, text/javascript, */*; q=0.01"})
    j_root = res.json()
    name_ssh_url_map = {}

    for j_item in j_root:
        name = j_item["name"]
        ssh_url = j_item["ssh_url"]
        name_ssh_url_map[name] = ssh_url

    for name, ssh_url in name_ssh_url_map.items():
        sub_dir = os.path.join(pwd, name)
        if os.path.isdir(sub_dir):
            my_util.subprocess_check_output(f"cd '{sub_dir}'", sub_dir)
        else:
            my_util.subprocess_check_output(f"git clone {ssh_url}", sub_dir)
        my_util.subprocess_check_output(f"cd '{pwd}'", sub_dir)

    my_util.subprocess_check_output(f"cd '{pwd}'", pwd)
    app_dir_list = []
    search_app_dir(pwd, app_dir_list)

    for app_dir in app_dir_list:
        build_success = False

        for new_dist_url_line in NEW_GRADLE_DISTRIBUTION_URL_LIST:
            my_util.subprocess_check_output(f"cd '{app_dir}'", app_dir)
            my_util.subprocess_check_output(f"chmod u+x ./gradlew", app_dir)
            file_path = os.path.join(app_dir, f"gradle/wrapper/gradle-wrapper.properties")

            file = open(file_path, f"r")
            line_list = file.readlines()
            file.close()

            file = open(file_path, f"w")

            for line in line_list:
                if f"distributionUrl" in line:
                    file.write(new_dist_url_line)
                else:
                    file.write(line)

            file.close()

            file_path = os.path.join(app_dir, f"local.properties")
            file = open(file_path, f"w")
            file.write(f"sdk.dir={home_dir}/Library/Android/sdk")
            file.close()

            try:
                my_util.subprocess_check_output(f"./gradlew :app:assembleDebug", app_dir)
                build_success = True
                break
            except Exception as e:
                build_success = False
                print(f"assembleDebug e:{e}")

        print(f"build !!! build_success:{build_success} app_dir:{app_dir}")

    if not options.install:
        return

    my_util.subprocess_check_output(f"cd '{pwd}'", pwd)
    my_util.subprocess_check_output(f"rm -rf apks", pwd)
    my_util.subprocess_check_output(f"mkdir apks", pwd)
    apk_file_list = []
    search_apk_file(pwd, apk_file_list)

    for apk_file in apk_file_list:
        token_list = apk_file.split("/")
        new_apk_name = None

        for token in reversed(token_list):
            if token in ["app-debug.apk", "debug", "apk", "outputs", "build", "app"]:
                continue
            new_apk_name = f"{token}.apk"
            my_util.subprocess_check_output(f"cp -v '{apk_file}' '{pwd}/apks/{new_apk_name}'", pwd)
            break

    for apk_file in apk_file_list:
        my_util.subprocess_check_output(f"adb install -r -t '{apk_file}'", pwd)



def search_apk_file(dir, apk_file_list):
    file_name_list = os.listdir(dir)
    for file_name in file_name_list:
        if file_name == "." or file_name == "..":
            continue
        sub_file = os.path.join(dir, file_name)

        if sub_file.endswith(".apk"):
            apk_file_list.append(sub_file)

        if os.path.isdir(sub_file):
            search_apk_file(sub_file, apk_file_list)


def search_app_dir(dir, app_dir_list):
    file_name_list = os.listdir(dir)

    for file_name in file_name_list:
        if file_name == "." or file_name == "..":
            continue
        sub_dir = os.path.join(dir, file_name)
        if os.path.isdir(sub_dir):
            sub_file_name_list = os.listdir(sub_dir)
            if "app" in sub_file_name_list and "gradlew" in sub_file_name_list:
                app_dir_list.append(sub_dir)
            else:
                search_app_dir(sub_dir, app_dir_list)


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:]))
