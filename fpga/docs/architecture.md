# FPGA版本架构设计

## 整体架构

### 计算核心架构
```

FPGA计算核心
├── 节点电压存储器 (BRAM)
├── 魔方约束引擎 (逻辑电路)
├── 静电松弛计算单元 (DSP)
├── 收敛检测模块 (状态机)
└── 控制接口 (AXI总线)

```

### 资源预估 (以Alveo U50为例)
| 资源类型 | 预估使用 | 可用总量 | 使用率 |
|---------|----------|----------|--------|
| LUT | 150K | 872K | 17% |
| FF | 200K | 1.7M | 12% |
| BRAM | 200 | 537 | 37% |
| DSP | 500 | 5,952 | 8% |

## 模块设计

### 节点网络模块
```verilog
module node_network #(
    parameter NODES = 64,
    parameter DATA_WIDTH = 16
)(
    input wire clk,
    input wire rst_n,
    input wire [DATA_WIDTH-1:0] initial_state [NODES],
    input wire [3:0] magic_pattern,
    output wire [DATA_WIDTH-1:0] node_voltages [NODES],
    output wire converged
);
    // 魔方约束处理
    magic_constraint_engine constraint_eng (...);
    
    // 松弛计算核心
    relaxation_core relax_core (...);
    
    // 收敛检测
    convergence_checker checker (...);
endmodule
```

魔方约束引擎

· 输入: 当前节点电压、魔方模式选择
· 处理: 计算魔线和偏差，生成调整量
· 输出: 各节点电压调整值

静电松弛计算

· 算法: 基于Jacobi迭代的并行计算
· 精度: 16位定点数运算
· 并行度: 全节点并行更新

性能目标

计算性能

· 节点规模: 64-256节点 (可配置)
· 收敛时间: < 1ms (典型问题)
· 吞吐量: 1000+问题/秒 (小规模)

能效目标

· 功耗: < 25W (FPGA核心)
· 能效比: 10x vs CPU实现
· 热设计: 被动散热可行
