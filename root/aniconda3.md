创建 Anaconda 环境的过程可以通过以下步骤完成：

1. **安装 Anaconda**：
   - 首先，访问 [Anaconda官网](https://www.anaconda.com/products/distribution) 下载适用于您操作系统的最新版本的 Anaconda 安装程序（通常为 Python 3.x 版本）。
   - 运行下载的安装程序，按照向导指示进行安装。

2. **打开终端或命令提示符**：
   - 在 Windows 上，可以按下 `Win + R` 键，然后输入 `cmd` 或 `Anaconda Prompt` 来打开 Anaconda 命令行界面。
   - 在 macOS 或 Linux 上，在终端中执行操作。

3. **创建新的虚拟环境**：
   - 使用以下命令创建一个名为 `nvh` 的新环境，并指定Python版本（例如Python 3.10）：
     ```shell
     conda create --name nvh python=3.10
     d:
     cd D:root
     pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
     py main.py
     ```
   - 其中 `nvh` 是您要给环境起的名字，您可以替换为您喜欢的任何名称。
   - `python=3.10` 指定使用Python 3.10版本。如果您希望使用其他Python版本，请相应地更改这个数字。

4. **激活环境**：
   - 创建环境后，需要激活它才能开始在这个环境中工作：
     - 对于 Windows:
       ```shell
       conda activate nvh
       ```
     - 对于 macOS/Linux:
       ```shell
       conda activate nvh
       ```

5. **检查环境是否已激活**：
   终端会显示当前活动环境的名称，即你刚才创建的环境名。

6. **在新环境中安装包**：
   - 在激活的环境下，您可以使用 `conda install` 或 `pip install` 命令来安装所需的库和软件包。
   - cd **root
   - pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

7. **退出环境**：
   - 当不再需要该环境时，可以使用以下命令退出：
     ```shell
     conda deactivate
     ```

这样就完成了通过Anaconda创建并管理虚拟环境的基本过程。