"""
魔方约束演示
展示魔方约束如何引导系统收敛行为
"""

import numpy as np
import matplotlib.pyplot as plt

def magic_constraint_demo():
    print("=== 魔方约束演示 ===\n")
    
    grid_size = 20
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    
    # 理论解
    theoretical_V = X**2 - Y**2
    
    # 定义魔线
    magic_lines = [{'type': 'row', 'index': 4}, {'type': 'col', 'index': 9}]
    magic_sum = 0.0
    
    # 初始化两个系统
    V_normal = np.zeros((grid_size, grid_size))
    V_magic = np.zeros((grid_size, grid_size))
    
    # 设置相同边界条件
    for V in [V_normal, V_magic]:
        V[0, :] = theoretical_V[0, :]
        V[-1, :] = theoretical_V[-1, :]  
        V[:, 0] = theoretical_V[:, 0]
        V[:, -1] = theoretical_V[:, -1]
    
    print("比较收敛过程...")
    max_iterations = 500
    tolerance = 1e-5
    
    errors_normal = []
    errors_magic = []
    
    for iteration in range(max_iterations):
        V_old_normal = V_normal.copy()
        V_old_magic = V_magic.copy()
        
        # 常规松弛
        V_normal[1:-1, 1:-1] = 0.25 * (
            V_old_normal[0:-2, 1:-1] + V_old_normal[2:, 1:-1] + 
            V_old_normal[1:-1, 0:-2] + V_old_normal[1:-1, 2:]
        )
        
        # 魔方约束松弛
        V_magic[1:-1, 1:-1] = 0.25 * (
            V_old_magic[0:-2, 1:-1] + V_old_magic[2:, 1:-1] + 
            V_old_magic[1:-1, 0:-2] + V_old_magic[1:-1, 2:]
        )
        
        # 应用魔方约束
        for line in magic_lines:
            if line['type'] == 'row':
                current_sum = np.sum(V_magic[line['index'], :])
                adjustment = (magic_sum - current_sum) / grid_size
                V_magic[line['index'], :] += adjustment
            else:  # column
                current_sum = np.sum(V_magic[:, line['index']])
                adjustment = (magic_sum - current_sum) / grid_size
                V_magic[:, line['index']] += adjustment
        
        # 保持边界
        for V in [V_normal, V_magic]:
            V[0, :] = theoretical_V[0, :]
            V[-1, :] = theoretical_V[-1, :]
            V[:, 0] = theoretical_V[:, 0]
            V[:, -1] = theoretical_V[:, -1]
        
        # 记录误差
        error_normal = np.max(np.abs(V_normal - theoretical_V))
        error_magic = np.max(np.abs(V_magic - theoretical_V))
        errors_normal.append(error_normal)
        errors_magic.append(error_magic)
        
        # 收敛检查
        change_normal = np.max(np.abs(V_normal - V_old_normal))
        change_magic = np.max(np.abs(V_magic - V_old_magic))
        
        if change_normal < tolerance and change_magic < tolerance:
            print(f"同时收敛于第 {iteration} 次迭代")
            break
    
    print(f"\n最终误差:")
    print(f"  常规系统: {errors_normal[-1]:.2e}")
    print(f"  魔方约束: {errors_magic[-1]:.2e}")
    
    # 验证魔线约束
    print("\n魔线约束验证:")
    for line in magic_lines:
        if line['type'] == 'row':
            actual_sum = np.sum(V_magic[line['index'], :])
            print(f"  第{line['index']+1}行和: {actual_sum:.6f}")
        else:
            actual_sum = np.sum(V_magic[:, line['index']])
            print(f"  第{line['index']+1}列和: {actual_sum:.6f}")
    
    # 可视化
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.semilogy(errors_normal, 'b-', label='Normal', alpha=0.7)
    plt.semilogy(errors_magic, 'r-', label='Magic Constraint', alpha=0.7)
    plt.xlabel('Iteration')
    plt.ylabel('Max Error')
    plt.title('Convergence Comparison')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 3, 2)
    plt.contourf(X, Y, V_normal, levels=20)
    plt.colorbar()
    plt.title('Normal Relaxation')
    
    plt.subplot(1, 3, 3)
    plt.contourf(X, Y, V_magic, levels=20)
    plt.axhline(y=y[4], color='red', linestyle='--', alpha=0.8, label='Magic Line')
    plt.axvline(x=x[9], color='orange', linestyle='--', alpha=0.8, label='Magic Line')
    plt.colorbar()
    plt.title('With Magic Constraints')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    magic_constraint_demo()
