#!/usr/bin/env python3
"""
天缠变项目结构重组脚本
自动将现有文件重新组织到新的文件夹结构中
"""

import os
import shutil
from pathlib import Path

def reorganize_project():
    print("开始重组天缠变项目结构...")
    
    # 新文件夹结构
    new_structure = {
        'asic': {
            'docs': ['architecture.md'],  # ASIC特定文档
            'design': [],  # 未来放设计文件
            'simulation': []  # 未来放仿真脚本
        },
        'fpga': {
            'docs': [],  # FPGA特定文档
            'src': [],   # HDL代码
            'constraints': []  # 时序约束
        },
        'common': {
            'docs': [
                'theoretical_foundation.md',
                'technical_verification.md', 
                'algorithm.md',
                'applications.md',
                'ROADMAP.md'
            ],
            'demos': [
                'demo_harmonic_tensor.py',
                'demo_electrostatic_relaxation.py',
                'demo_magic_constraint.py'
            ],
            'src': [],  # 共享算法代码
            'tests': []  # 测试用例
        }
    }
    
    # 创建文件夹结构
    for main_dir, sub_dirs in new_structure.items():
        Path(main_dir).mkdir(exist_ok=True)
        for sub_dir in sub_dirs:
            Path(main_dir, sub_dir).mkdir(exist_ok=True)
            print(f"创建文件夹: {main_dir}/{sub_dir}")
    
    # 移动文档文件
    docs_mapping = {
        'docs/architecture.md': 'asic/docs/',
        'docs/theoretical_foundation.md': 'common/docs/',
        'docs/technical_verification.md': 'common/docs/',
        'docs/algorithm.md': 'common/docs/',
        'docs/applications.md': 'common/docs/',
        'ROADMAP.md': 'common/docs/'
    }
    
    for src, dst in docs_mapping.items():
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"移动: {src} -> {dst}")
    
    # 移动演示代码
    demos_mapping = {
        'demos/': 'common/demos/'
    }
    
    for src, dst in demos_mapping.items():
        if os.path.exists(src):
            for file in os.listdir(src):
                shutil.move(os.path.join(src, file), dst)
            os.rmdir(src)  # 删除空文件夹
            print(f"移动文件夹: {src} -> {dst}")
    
    # 更新README中的链接
    update_readme_links()
    
    print("项目结构重组完成！")

def update_readme_links():
    """更新README.md中的文档链接"""
    readme_path = 'README.md'
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 替换文档链接路径
        link_mapping = {
            'docs/architecture.md': 'asic/docs/architecture.md',
            'docs/theoretical_foundation.md': 'common/docs/theoretical_foundation.md',
            'docs/technical_verification.md': 'common/docs/technical_verification.md',
            'ROADMAP.md': 'common/docs/ROADMAP.md'
        }
        
        for old_link, new_link in link_mapping.items():
            content = content.replace(old_link, new_link)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("README链接更新完成")

if __name__ == "__main__":
    reorganize_project()
