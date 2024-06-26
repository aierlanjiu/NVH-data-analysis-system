<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://user-images.githubusercontent.com/1651790/224081217-86521beb-1b69-4071-b195-f2ce0bb33db7.png">
  <img alt="NebulaGraph Data Intelligence Suite(ngdi)" src="https://user-images.githubusercontent.com/1651790/224081979-d3aa7867-94a6-4a85-a5d7-603e02360cee.png">
</picture>
<p align="center">
    <br> 中文 | <a href="README.md">English</a>
</p>
<p align="center">
    <em>The translator that does more than just translation - powered by OpenAI.</em>
</p>

<p align="center">
  <a href="LICENSE" target="_blank">
    <img alt="MIT License" src="https://img.shields.io/github/license/yetone/openai-translator.svg?style=flat-square" />
  </a>

  <!-- TypeScript Badge -->
  <img alt="TypeScript" src="https://img.shields.io/badge/-TypeScript-blue?style=flat-square&logo=typescript&logoColor=white" />

  <!-- Python Badge -->
  <img alt="Python" src="https://img.shields.io/badge/-Python-blue?style=flat-square&logo=python&logoColor=white" />

  <!-- Tkinter Badge -->
  <img alt="Tkinter" src="https://img.shields.io/badge/-Tkinter-blue?style=flat-square&logo=python&logoColor=white" />

  <!-- Qt Badge -->
  <img alt="Qt" src="https://img.shields.io/badge/-Qt-blue?style=flat-square&logo=qt&logoColor=white" />

  <!-- Windows Badge -->
  <a href="https://github.com/yetone/openai-translator/releases" target="_blank">
    <img alt="Windows" src="https://img.shields.io/badge/-Windows-blue?style=flat-square&logo=windows&logoColor=white" />
  </a>


</p>


[![Conventional Installation Method](https://img.shields.io/static/v1?label=&message=Conventional%20Installation%20Method&color=gray)]
## 项目简介
本项目旨在开发一款适用于Windows操作系统的可交互软件，专为汽车行业设计，用于处理效率数据、NVH半消音室数据、EOL产线数据以及整车噪声数据分析。该软件采用Python语言编写，并利用Tkinter或Qt框架构建直观且功能丰富的图形用户界面（GUI）。同时，软件集成了数据库系统以支持数据的导入、存储和检索。

## 功能模块

### 1. 效率数据处理模块
- 数据导入：提供多种格式的数据文件导入接口。
- 数据分析：包括数据清洗、整理、统计计算与可视化展示功能。
- 结果输出：支持导出至Excel、PDF等格式，并实时显示关键指标。

### 2. NVH半消音室数据处理模块
- 数据/工况/测点/样机/分析阶次/目标导入：全面支持各类参数输入。
- 高级数据分析：进行频域、时域分析及NVH特性深入研究。
- 报告编制与输出：内置报告编辑器，自动生成专业报告并支持预览、打印和导出。

### 3. EOL产线数据处理模块
- 数据及参数导入：兼容EOL生产线特定数据结构，具有灵活配置能力。
- 拟合与数据分析：扩展模型拟合功能，对生产线上采集的数据进行深度分析。
- 报告生成与输出：同样具备报告编制工具，并根据EOL特点定制报告内容。

### 4. 整车噪声数据分析模块
- 数据导入：支持音频文件和其他噪声相关数据的导入。
- 音频回放：集成音频播放器，方便回放原始音频数据。
- 音频Colormap输出：将音频信号转换成可视化图像，如声压级谱图。

```plaintext
root/
├── main.py  # 主程序入口，负责整体流程控制与GUI初始化
├── config.py  # 配置程序
├── __init__.py #初始化
├── gui/
│   ├── __init__.py
├── data_management/
│   ├── __init__.py
│   ├── data_init.py  # 创建数据副本
│   ├── data_loader.py  # 数据加载模块，读取并解析各类数据文件
├── data_processing/
│   ├── __init__.py
│   ├── efficiency_data.py  # 效率数据分析模块
│   ├── semiacoustic.py  # NVH半消音室数据分析模块
│   ├── eol_data.py  # EOL产线数据分析模块
│   └── fitting_curve.py  # EOL产线数据目标拟合
├── visualization/
│   ├── __init__.py
│   |── eol_plot.py  # 数据可视化模块
|   |── noise_plot.py  # 数据可视化模块
└── reports/
    ├── __init__.py
    └── report_generation.py  # 报告生成模块，自动生成并导出报告
```
# main.py 示例内容概览

按照aniconda3教程设置好运行环境 输入py main.py 运行程序
如果aniconda3提示无法导入PIL 请在VSCODE中运行main.py


### 🌟 Star History
[![Star History Chart](https://api.star-history.com/svg?repos=aierlanjiu/NVH-data-analysis-system&type=Date)](https://star-history.com/#aierlanjiu/NVH-data-analysis-system&Date)