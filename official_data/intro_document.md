# Data Mining Project 1
###### tags: `admin`

### Programming (60 points)

 
1. FP-Tree (40 points)
2. Apriori (20 points)
3. TAs will test your algorithms with our testdata and with different hyperparameters (each combination is a testcase); there will be a total of 10 testcases. Passing 1 (rounding to 2 decimal places, `_.__`) earns you 4 points in FP-Tree; 2 points in Apriori. 
    
### Report  (40 points)

Generate your own dataset with the IBM Generator (see `IBM_Quest_Synthetic_Data_Generator_使用教學.pdf` on Moodle) to test your algorithms. 

Find and answer (40 points)
- 1.1 What do you observe in the below 4 scenarios? What could be the reason? 
(For both support and confidence, you should set 0.1 for low and 0.7 or more for high)
    - High support, high confidence 
    - High support, low confidence
    - Low support, low confidence 
    - Low support, high confidence
- 1.2 Runtime statistics
    - Report the run time for both algorithms for the above 4 scenarios in a table. 
    - Try to provide an explanation for the runtime statistics. 
- 1.3 Any topics you are interested in

 ### Bonus (20 points)

Experiment with other dataset(s) selected from Kaggle/UCI. 
- Apply your algorithms to another dataset from Kaggle or UCI.
- Do some experiments (eg. observe the 4 scenarios as requested for other datasets). 
- Make sure to specify the name of self-selected dataset(s), and include your discoveries in the report.

---

## Programming Language
You could choose any programming language you are familiar with for this project. The core idea is you should not use packages written by others as your submitted homework (you can use them for your own testing). 
- Python3:
    - Please make sure your python version is >= 3.7. 
    - You can only use the [built-in-library](https://docs.python.org/3.7/library/) in the programming implementation. Any other imports that requires extra installation gain minus 5 points for each. 
 
- Other programming languages:
    - Please schedule a time with TAs (nckudm@gmail.com) to come to IKM Lab (65903, CSIE New Building) for project demo. You should be able to generate files in the format specified below. We will grade your newly-generated outputs with our testing script. 

---

## Submission
- Deadline
    - **Oct 17, 2023 9:00**. 
    - Late submission within 1 week will get a 10% discount, and 3 weeks will get a 30% discount. Submissions later than that gains 40% discount.
- Structure 
    - Please make sure that your project contains `main.py` file, `inputs` directory and `outputs` directory. 
   - Your should submit a `.zip` file with the name `{student_id}_DM_Project1` (eg. `P1234567_DM_Project1`). It should be unzipped into a directory with the same name, and the directory structure should be: 
   ```c
    {student_id}_DM_Project1
        ├── inputs (directory for input files)
        │   ├── kaggle.txt
        │   └── ibm-2021.txt
        ├── main.py
        ... (if you have other module)
        └── outputs (directory for output files)
            ├── kaggle-apriori.csv (result of aprior algorithm applied on kaggle.txt)
            ├── kaggle-fp_growth.csv (result of fp_growth algorithm applied on kaggle.txt)
            ├── ibm-2021-apriori.csv (result of aprior algorithm applied on ibm-2021.txt)
            └── ibm-2021-fp_growth.csv (result of fp_growth algorithm applied on ibm-2021.txt)
   ```
- Template
    - The suggested code template following the above directory structure can be accessed here: [hw1_example_2023.zip](https://drive.google.com/file/d/1zxO5u9B2hijgoO1Au1e1iY5XpJKCmsu1/view?usp=sharing). 
    - Note that there're some imprecisions in terms of data format information, please refer to the explanation in `IBM_Quest_Synthetic_Data_Generator_使用教學.pdf` as standard version.  
- Requirements
    - We will execute your code with the following: 
    ```shell
    cd {student_id}_DM_Project1
    python3 main.py --dataset=ibm-2021.txt --min_sup=0.05 --min_conf=0.05
    ```
     - Dataset: Our grading data will be generated following the parameters as below (except `randseed`), and so is the released data. You can use it to check your algorithms or generate your own. 
         - You can get the released data from here: [ibm-2023-released.txt](https://drive.google.com/file/d/1eTEMyk4MybKxS9atWMNan7s4cu-Y5rzK/view?usp=sharing)
    ```
        lit -fname {dataset_name} -ntrans 3 -tlen 14  -randseed -87 -conf 0.3 -nitems 0.05
    ```
    - Hyperparameters: `min_sup` and `min_conf` will be arbitrary; we guarantee they will be larger than 0.05 (with the dataset generated following the above command). Please make sure your code successfully delivers the result at these thresholds.
    - Runtime: 5 min/testcase. If your code crashes or runs longer than 5 minutes on 1 testcase, you fail that testcase. 
    - Output: 
        - We expect to see 2 newly-generated files looking like
        ```
        outputs/ibm-2021-fp-growth-{}-{}.csv
        outputs/ibm-2021-apriori-{}-{}.csv
        ``` 
        after executing your code. If you print the results instead of writing to files; write to files with different names, ... You will not get points. 
        - They should be in the format specified in `utils.write_file()` function. 
        - We will use `grading.py` included in the above template to grade your outputs. 

---
    
## The most important thing: DON'T CHEAT 
If you cheat (copy others' works extensively, including code online) on this project, you will get a 0 in this homework. 