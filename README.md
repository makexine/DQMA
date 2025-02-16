# DQMA

Existing Retrieval-Augmented Generation (RAG) methods encounter inherent limitations when applied to LLM for task planning, particularly in discerning between contextually similar but semantically opposing sentences. 
To address this challenge, we introduce the Data-Quality-Managed Agent (DQMA), which fuses an LLM with RAG and implements data quality management on the retrieved texts, converting natural instructions into plans for robots.

## Run DQMA 

### Generate Dataset
```Bash
python knowledge_generate/generate_knowledge.py
```

### Generate embeddings of the knowledge base
```Bash
python generate_passage_embeddings.py
```

### Retrieve Contexts
```Bash
python passage_retrieve.py
```

### Retrieve Contexts after QMRA
```Bash
python src_trimmer/vmdit_retrieval.py
```

### Run the LLM planer
```Bash
python LLM/intsr2goal_test_main.py    #Large parameter LLM
python LLM/intsr2goal_test_main_s.py  #Small parameter LLM
```
Mode 'base','rag','qmra' refers to the basic LLM planner, RAG LLM planner and QMRA planner.

### Select $\theta$
```Bash
python select_thre/roc.py 
```


## 测试集构造思路清单

### 测试集种类

#### 咖啡厅（参考）
- **动作（Actions）**
  - 移动（Move）
    - arg: walk; walktowards
    - arg: walktoword; turnleft; turnright
  - 操作（Manipulation）
    - grab; open; close; put; putin; switchon; switchoff; touch; drink; lookat

- **对象（Objects）**
  - 食物（Food）
    - Apple, Banana, Orange, Peach, Pear, BellPepper, Carrot, Cucumber, Potato, Tomato, Chicken, Salmon, Bread, Bread_slice, Pancake, Chips, Salad, Coffee_pot, Milk, Alcohol, Beer, Bottle_water, Wine, ChocolateSyrup, Cereal
  - 烹饪器具（Cooking Tools）
    - ChefKnife, FryingPan, Stove, Toaster, Kettle, Microwave, Cutting_board
  - 就餐器具（Dining Utensils）
    - Cutlery_Knife, Cutlery_fork, Spoon, Dish_bowl, Plate, Mug, WaterGlass, WineGlass, Napkin, PaperTowel
  - 家具（Furniture）
    - Chair, Desk, DiningTable, Kitchen_table, Nightstand, Shelf, Sofa
  - 家电（Appliances）
    - CeilingFan, Ceiling_lamp, Fridge, Dishwasher, Kettle, Microwave, OvenTray, Stove, Toaster, Washing_machine
  - 装饰（Furnishings）
    - Curtains, WallPictureFrame, WallTV, Wall_lamp, Wall_phone
  - 开关（Controls）
    - LightSwitch, Power_socket

- **谓词结构（predicate_condition）**
  - 0 arg:
    - walkforward; turnleft; turnright; standup
  - 1 arg:
    - walk_<object>; walktowards_<object>; sit_<furniture>; grab_<item>; open_<item>; close_<item>; put_<item>_<furniture>; putin_<item>_<appliance>; switchon_<appliance>; switchoff_<appliance>; touch_<item>; drink_<beverage>; lookat<item>

- **例句（few-shot）**
  - walktowards_Chair; sit_Chair; sit_Sofa; grab_Apple; grab_ChefKnife;
  - open_Fridge; close_Door; put_Bread_Plate; putin_Apple_Bowl;
  - switchon_Microwave; switchoff_Toaster; touch_WallPictureFrame;
  - drink_Coffee_pot; drink_Bottle_water; lookat_Tomato;

### 客厅
- **动作（Actions）**
  - 移动（Move）
    - 1 arg：walk; walktowards
    - 0 arg：walktoword; turnleft; turnright
  - 操作（Manipulation）
    - grab; open; close; put; putin; switchon; switchoff; touch; drink; lookat
- **对象（Objects）**
  - 家具（Furniture）
    - Chair, Sofa, Coffee_table, TV_stand, Nightstand, BookShelf
  - 家电（Appliances）
    - CeilingFan, Ceiling_lamp, Table_lam, WallTV, Radio, Printer, Projector, Power_socket
  - 装饰（Furnishings）
    - WallPictureFrame, Clock, Vase, PhotoFrame, LotionBottle, Perfume
  - 日常用品（Daily Items）
    - Pen, Notebook, Magazine, Book, Boardgame, Cards, TeddyBear, Toy
  - 饮食相关（Food & Beverage Related）
    - WaterGlass, WineGlass, Mug, Bottle_waterm, Beer, Wine, Coffee_pot
  - 个人护理用品（Personal Care Items）
    - Toothbrush, Toothpaste, Towel, HairProduct, FaceCream
  - 其他（Miscellaneous）
    - Cellphone, Computer, CPU_screen, Coatack, Window, Faucet, Garbage_can

- **谓词结构（predicate_condition）**
  - walktowards_<furniture>, grab_<daily_item>, open_<furniture>,
  - close_<furniture>, put_<daily_item>_<furniture>,
  - putin_<daily_item>_<appliance>, switchon_<appliance>
  - switchoff_<appliance>, touch_<furnishing>, drink_<beverage>,
  - lookat<furnishing>

- **例句（few-shot）**
  - touch_Napkin && put_Napkin_Plate ：(用餐完毕后)轻触餐巾并把它放在盘旁边
  - grab_Cutlery_fork && grab_Spoon ：(为用餐准备餐具)拿起叉子和勺子准备用餐
  - walkto_Kitchen_table && grab_Chicken & put_Chicken_Plating ：(走到厨房的桌前，取鸡，并将其放置到服务盘中准备端给顾客)
  - putin_Plate_Dishwasher && open_Dishwasher ：将盘子放进洗碗机并打开洗碗机
  - put_Bread_slice_Plate || putin_Carrot_Dish_bowl ：在盘中放面包片或者把胡萝卜放进碗中

### 卧室
- **动作（Actions）**
  - 移动（Move）
    - walktowards_Bed; sit_Bed
  - 操作（Manipulation）
    - grab_Pajamas; put_Pajamas_Body : 从衣柜或抽屉拿出睡衣穿上。
  - turnoff_LightSwitch : 关闭房间的灯光
  - sit_Sofa; grab_Book; lookat_Book : 坐在沙发上拿起本书开始阅读。
  - grab_WaterGlass; drink_WaterGlass : 拿起水杯喝水
  - open_Nightstand; grab_Pen; close_Nightstand : 打开夜桌抽屉取出笔后再次关上。
  - put_Clothes_pants_Drawer; put_Clothes_shirt_Drawer : 将裤子和衬衫放进抽屉中
  - grab_Cellphone; lookat_Cellphone : 拿起手机查看信息。
  - switchon_PC; switchoff_PC : 打开或关闭电脑
  - walkto_Standing_mirror; lookat_Standing_mirror : 走到立镜前照镜子检查外观
  - grab_Dumbbell; lift_Dumbbell : 拿起哑铃做些简单的举重练习。
  - use_Balance_ball : 使用平衡球进行锻炼
  - feed_Cat; pet_Cat : 喂猫并抚摸它
  - grab_Vacuum_cleaner; clean_Floor : 拿起吸尘器打扫地面。
  - grab_Duster; dust_Shelf : 拿起除尘器清理架上的灰尘

- **谓词结构（predicate_condition）**
  - 0 arg:
  - walkforward; turnleft; turnright; standup
  - 1 arg:
  - walk_<object>; walktowards_<object>; sit_<furniture>; grab_<item>;
  open_<item>; close_<item>; put_<item>_<furniture>;
  putin_<item>_<appliance>; switchon_<appliance>; switchoff_<appliance>;
  touch_<item>; drink_<beverage>; lookat<item>;
