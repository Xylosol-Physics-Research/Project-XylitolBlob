"""
静电松弛算法演示
演示通过迭代松弛法求解拉普拉斯方程
"""

import numpy as np
import matplotlib.pyplot as plt

def electrostatic_relaxation_demo():
    print("=== 静电松弛算法演示 ===\n")
    
    # 创建网格
    grid_size = 20
    V = np.zeros((grid_size, grid_size))
    
    # 设置坐标和理论解
    x = np.linspace(-1, 1, grid_size)
    y = np.linspace(-1, 1, grid_size)
    X, Y = np.meshgrid(x, y)
    theoretical_V = X**2 - Y**2  # 调和函数
    
    # 设置边界条件
    V[0, :] = theoretical_V[0, :]    # 上边界
    V[-1, :] = theoretical_V[-1, :]  # 下边界  
    V[:, 0] = theoretical_V[:, 0]    # 左边界
    V[:, -1] = theoretical_V[:, -1]  # 右边界
    
    print("开始松弛迭代...")
    max_iterations = 1000
    tolerance = 1e-5
    
    for iteration in range(max_iterations):
        V_old = V.copy()
        
        # Jacobi迭代
        V[1:-1, 1:-1] = 0.25 * (V_old[0:-2, 1:-1] + V_old[2:, 1:-1] + 
                                V_old[1:-1, 0:-2] + V_old[1:-1, 2:])
        
        # 保持边界条件
        V[0, :] = theoretical_V[0, :]
        V[-1, :] = theoretical_V[-1, :]
        V[:, 0] = theoretical_V[:, 0]
        V[:, -1] = theoretical_V[:, -1]
        
        # 检查收敛
        max_change = np.max(np.abs(V - V_old))
        if max_change < tolerance:
            print(f"收敛于第 {iteration} 次迭代")
            break
            
    # 计算最终误差
    final_error = np.max(np.abs(V - theoretical_V))
    print(f"最终最大误差: {final_error:.2e}")
    
    # 可视化
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 3, 1)
    plt.contourf(X, Y, theoretical_V, levels=20)
    plt.colorbar()
    plt.title('Theoretical Solution')
    
    plt.subplot(1, 3, 2)
    plt.contourf(X, Y, V, levels=20)
    plt.colorbar()
    plt.title('Numerical Solution')
    
    plt.subplot(1, 3, 3)
    error_map = plt.contourf(X, Y, np.abs(V - theoretical_V), levels=20)
    plt.colorbar(error_map)
    plt.title('Absolute Error')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    electrostatic_relaxation_demo()
