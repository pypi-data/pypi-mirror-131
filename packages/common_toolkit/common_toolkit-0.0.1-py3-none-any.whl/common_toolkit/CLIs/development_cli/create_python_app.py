import fire
import os


class CreatePythonApp:
    """
    创建不同类型的python项目骨架
    """
    @staticmethod
    def create_python_basic_skeleton(
                                   project_name: str,
                                   template_url: str
                                   ):
        """
        创建基本的python项目骨架，eg：`create_python_basic_skeleton project_name template_url`

        Args:
            project_name: 项目名称
            template_url: 项目模板地址，支持自定义项目模板

        Returns:

        """
        print(f"Cloning into '{project_name}'...")
        os.system(f"git clone {template_url} {project_name}")
        print("delete the skeleton .git directory")
        os.system(f"rm -rf ./{project_name}/.git")
        os.system(f"git init ./{project_name}")
        print(f"Initialized empty Git repository in {os.path.abspath(f'{project_name}')}/")
        os.system(f"git init ./{project_name}")
        os.system(f"pip install pre-commit")
        os.system(f"pre-commit install")
        print("""
        Docs:
                代码正常执行 `$git add/commit` 操作，即会自动执行pre-commit操作，
                其中包含一些静态格式化。如果commit失败，提示文件被修改，尝试重新git add/commit 即可
        """)


# flit shell命令入口
def main():
    fire.Fire(CreatePythonApp)


if __name__ == "__main__":
    fire.Fire(CreatePythonApp)
