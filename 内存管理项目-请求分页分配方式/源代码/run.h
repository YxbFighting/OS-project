#pragma once
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <conio.h>
#include <string>
#include <queue>
#include <vector>
#include <algorithm>
#include "image.h"
using namespace std;

#define MAX_NUM 4
#define TASK_NUM 320

struct block
{
	int page_num = 0;
	string block_num = "";
	int status = 0;  //0²»ÔÚ 1ÔÚ
	string location_out = "";
};
struct block_lru
{
	int page_num = 0;
	int num = 330;
};

int cal_instruction(int ini_ins, int position);
void initial(block page_table[32]);
void exchange(block page_table[32], vector<int>& memory_block, vector <int>& visit_record, int page_num, int method, block_lru lru_box[4], int i);
void draw_block(int x, int y, int page_num);
void show_pro(vector<int> memory_block, int page_num);
void visit(block page_table[32], vector<int>& memory_block, block& ini_block, int block_tag, vector <int>& visit_record, int method, int& loss, char method_abc, block_lru lru_box[4], int i);
int to_be_continued(string a);
int run();