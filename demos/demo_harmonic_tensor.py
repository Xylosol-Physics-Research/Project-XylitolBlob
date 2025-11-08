调和张量验证演示
验证四极张量 M_ik = 3*x_i*x_k - r^2 * δ_ik 的调和性质
"""

import numpy as np

def harmonic_tensor_demo():
    print("=== 调和张量验证演示 ===\n")
    
    # 测试点
    x, y, z = 1.5, 0.8, -0.5
    r_sq = x**2 + y**2 + z**2
    
    # 计算四极张量
    M = np.array([
        [3*x*x - r_sq, 3*x*y, 3*x*z],
        [3*y*x, 3*y*y - r_sq, 3*y*z], 
        [3*z*x, 3*z*y, 3*z*z - r_sq]
    ])
    
    print(f"坐标点: ({x}, {y}, {z})")
    print("四极张量 M_ik:")
    for i, row in enumerate(M):
        print(f"  M[{i}] = [{row[0]:8.4f}, {row[1]:8.4f}, {row[2]:8.4f}]")
    
    # 数值验证拉普拉斯算子
    print("\n验证调和性 (ΔM_ik = 0):")
    h = 1e-5
    coords = [x, y, z]
    
    for i in range(3):
        for k in range(3):
            laplacian = 0
            for dim in range(3):
                # 计算二阶偏导
                points_plus = coords.copy()
                points_minus = coords.copy()
                points_plus[dim] += h
                points_minus[dim] -= h
                
                M_plus = calculate_M_ik(i, k, *points_plus)
                M_minus = calculate_M_ik(i, k, *points_minus)
                M_center = calculate_M_ik(i, k, *coords)
                
                second_deriv = (M_plus - 2*M_center + M_minus) / (h**2)
                laplacian += second_deriv
            
            status = "✓" if abs(laplacian) < 1e-6 else "✗"
            print(f"  ΔM[{i},{k}] = {laplacian:12.6e} {status}")

def calculate_M_ik(i, k, x, y, z):
    """计算四极张量分量"""
    r_sq = x*x + y*y + z*z
    if i == k:
        return 3 * [x, y, z][i]**2 - r_sq
    else:
        return 3 * [x, y, z][i] * [x, y, z][k]

if __name__ == "__main__":
    harmonic_tensor_demo()
