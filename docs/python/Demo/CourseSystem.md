# 课程系统

## 任务需求

角色：学校、学员、课程、讲师

要求：

1. 创建北京、上海2所学校。
2. 创建Linux、Python、go三个课程，Linux和Python在北京开，go在上海开。
3. 课程包含周期、价格，通过学校创建课程。
4. 通过学校创建班级，班级关联课程、讲师。
5. 创建讲师。
5. 创建学员时，选择学校，关联班级。
6. 创建讲师角色（不需要关联学校）。
7. 提供两个角色接口。
    1. 学员视图：可以注册，交学费，选择班级。
    2. 讲师视图：讲师可以管理自己的班级，上课时选择班级，查看班级学员列表，修改所管理的学员的成绩。
    3. 管理视图：创建讲师，创建班级，创建课程。
8. 上述操作所产生的数据通过pickle保存到文件。


## 需求分析

1. 管理视图

    1. 注册
    2. 登录
    3. 创建学校
    4. 创建课程（先选择学校）
    5. 创建讲师

2. 学员视图

    1. 注册
    2. 登录功能
    3. 选择校区
    4. 选择课程（先选择校区，在选择校区中的某一门课程，选择课程即选择班级）
        * 学生选择课程，课程也选择学生
    5. 查看分数
    6. 交学费

3. 讲师视图

    1. 登录
    2. 查看教授课程
    3. 选择教授课程
    4. 查看课程下的学生
    5. 修改学生分数




## 架构设计（三层架构）

* 用户视图层
    * 用于与用户进行交互。
    * 实现简单的逻辑判断，比如注册功能中两次密码是否一致的校验。
    * core
        * src.py 主视图
        * admin.py: 管理视图
        * student.py: 学员视图
        * teacher.py: 讲师视图
* 逻辑接口层
    * 核心业务逻辑的处理
    * interface
        * admin_interface.py
        * studeng_interface.py
        * teacher_interface.py
* 数据处理层
    * 数据处理，比如增删改查。
    * db
        * models.py
        * db_handler.py
            * pickle保存对象
            * object --> pickle

## 文件结构：

    /--conf/
    |    |--settings.py
    |
    |--core/
    |    |--src.py
    |    |--admin.py
    |    |--student.py
    |    |--teacher.py
    |
    |--db/
    |    |--models.py
    |    |--db_handler.py
    |        |--pickle
    |
    |--interface/
    |    |--admin_interface.py
    |    |--student_interface.py
    |    |--teacher_interface.py
    |
    |--lib/
    |    |--common.py
    |
    |--readme.md
    |
    |--start.py


