#include <iostream>
#include <iomanip>
#include <cstdio>
#include <conio.h>
#include <string>
#include <queue>
#include <vector>
#include <algorithm>
#include "image.h"
#include "run.h"
using namespace std;

#define MAX_NUM 4
#define TASK_NUM 320

int cal_instruction(int ini_ins, int position)
{
	int ans = 0;
	if (position % 2 == 0)
		ans = ini_ins + 1;
	else if (position % 4 == 1)
		ans = rand() % ini_ins;
	else if (position % 4 == 3)
		ans = (rand() % (TASK_NUM - ini_ins - 1)) + ini_ins + 1;
	if (ans >= TASK_NUM)
		ans = rand() % 320;
	return ans;
}

void initial(block page_table[32])
{
	string block_ini = "00800";
	for (int i = 0; i < 32; i++) {
		// block_ini[4] += 1;
		page_table[i].page_num = i;
		page_table[i].block_num = block_ini;
		page_table[i].location_out = page_table[i].block_num + "000";
	}
}

void exchange(block page_table[32], vector<int>& memory_block, vector <int>& visit_record, int page_num, int method, block_lru lru_box[4], int i)
{
	if (method == 1) {
		cout << "ҳ��Ϊ" << page_table[memory_block[0]].page_num << "��ҳ�������ڴ�,ҳ��Ϊ" << page_num << "��ҳ�������ڴ�!" << endl;
		page_table[memory_block[0]].status = 0;
		vector<int>::iterator k = memory_block.begin();
		memory_block.erase(k);
		memory_block.push_back(page_num);
	}
	else {
		int mintag = 0x3f3f3f, tag = 0;
		for (int j = 0; j < 4; j++) {
			if (lru_box[j].num < mintag) {
				mintag = lru_box[j].num;
				tag = j;
			}
		}
		cout << "ҳ��Ϊ" << lru_box[tag].page_num << "��ҳ�������ڴ�,ҳ��Ϊ" << page_num << "��ҳ�������ڴ�!" << endl;
		page_table[lru_box[tag].page_num].status = 0;
		memory_block[tag] = page_num;
		lru_box[tag].page_num = page_num;
		lru_box[tag].num = i;
	}
}

void draw_block(int x, int y, int page_num)
{
	cct_setcursor(CURSOR_INVISIBLE);

	int bgc[8] = { 2,14,3,4,5,6,12,10 };
	int fc[4] = { 0,1,8,9 };
	int bg = bgc[page_num % 8];
	int f = fc[page_num / 8];
	cct_showstr(x, y, "        ", bg, f, 1, -1);

	cct_showstr(x, y + 1, "   ", bg, f, 1, -1);
	if (page_num < 10) {
		cct_showstr(x + 3, y + 1, " ", bg, f, 1, -1);
		cct_showch(x + 4, y + 1, char('0' + page_num), bg, f, 1);
	}
	else
		cout << page_num;

	cct_showstr(x + 5, y + 1, "   ", bg, f, 1, -1);

	cct_showstr(x, y + 2, "        ", bg, f, 1, -1);

	cct_setcursor(CURSOR_VISIBLE_NORMAL);
	cct_setcolor();
}

void show_pro(vector<int> memory_block, int page_num)
{
	for (int i = 0; i < memory_block.size(); i++) {
		draw_block(4 + 9 * i, 9, memory_block[i]);
	}
	cct_gotoxy(0, 20);
}

void visit(block page_table[32], vector<int>& memory_block, block& ini_block, int block_tag, vector <int>& visit_record, int method, int& loss, char method_abc, block_lru lru_box[4], int i)
{
	cout << "����ָ��λ�� : ";
	if (ini_block.status == 1) {
		visit_record.push_back(ini_block.page_num);
		cout << "��ָ������ҳ���ڴ��ڣ�������е���!" << endl;
		cout << "��ָ��������ַΪ : ";

		for (int j = 0; j < 4; j++) {
			if (lru_box[j].page_num == ini_block.page_num) {
				lru_box[j].num = i;
				break;
			}
		}

		cout << "008" << (ini_block.page_num >= 16) << ' ';
		if (ini_block.page_num % 16 < 10)
			cout << ini_block.page_num % 16;
		else
			cout << char('A' + ini_block.page_num % 16 - 10);
		cout << 0 << (block_tag * 4) / 16;
		if ((block_tag * 4) % 16 % 16 < 10)
			cout << (block_tag * 4) % 16 % 16;
		else
			cout << char('A' + (block_tag * 4) % 16 % 16 - 10);

		cout << 'H' << endl;
	}
	else {
		cout << "�����ڴ��ڣ�ȱҳ!" << endl;
		loss++;
		ini_block.status = 1;
		if (memory_block.size() < 4) {
			memory_block.push_back(ini_block.page_num);
			lru_box[memory_block.size() - 1].page_num = ini_block.page_num;
			lru_box[memory_block.size() - 1].num = i;
		}
		else
			exchange(page_table, memory_block, visit_record, ini_block.page_num, method, lru_box, i);
		cout << "���ڴ��е�ҳ��ҳ��Ϊ : ";
		for (int i : memory_block)//���
		{
			cout << i << " ";
		}
		cout << endl;
	}
	cout << endl;
	if (method_abc == 'A')
		show_pro(memory_block, ini_block.page_num);
}

int to_be_continued(string a)
{
	cct_setcolor(); //�ָ�ȱʡ��ɫ
	cout << endl;

	cout << a;

	/* ���Գ��س�������������루ע�⣺_getch�Ļس���\r����getchar��\n��*/
	while (char get = _getch()) {
		if (get == 'q' || get == 'Q') {
			cout << endl;
			return 1;
		}
		else if (get == '\r')
			break;
	}


	return 0;
}

int run()
{
	string ini_physic_loc = "00800000";  //ʮ�����Ƴ�ʼ��ַ
	block page_table[32];
	vector <int> visit_record;
	int method_of_exchange = 1, loss = 0;
	vector <int> memory_block;
	srand((int)time(0));
	int ins = rand() % 320;
	block_lru lru_box[4];

	initial(page_table);

	char method;

	cout << "======================================================" << endl;
	cout << "                   ��ѡ��ָ��ִ�з�ʽ                 " << endl;
	cout << "======================================================" << endl;
	cout << "             A.��ִ��ָ��(320��)                    " << endl;
	cout << "             B.һ����ִ��320��ָ��                    " << endl;
	cout << "             C.һ����ִ�и���ҵ��ȫ��ָ��             " << endl;
	cout << "             D.�˳�ģ�����                           " << endl;
	cout << "======================================================" << endl;

	while (1) {
		cout << "������ִ�з�ʽ : ";
		cin >> method;
		if (method == 'd' || method == 'D')
			return 1;
		if (cin.good() && ((method >= 'A' && method <= 'C') || (method >= 'a' && method <= 'c'))) {
			if (method >= 'a' && method <= 'c')
				method += 'A' - 'a';
			cin.clear();
			cin.ignore(65355, '\n');
			break;
		}
		else {
			cout << "����������������룡" << endl;
			cin.clear();
			cin.ignore(65355, '\n');
		}
	}

	cct_cls();

	cout << "======================================================" << endl;
	cout << "                   ��ѡ��ҳ���û��㷨                 " << endl;
	cout << "======================================================" << endl;
	cout << "             1.FIFO�Ƚ��ȳ�ҳ���û��㷨               " << endl;
	cout << "             2.LRU������δʹ���㷨                  " << endl;
	cout << "======================================================" << endl;

	while (1) {
		cout << "������ִ�з�ʽ : ";
		cin >> method_of_exchange;
		if (cin.good() && (method_of_exchange == 1 || method_of_exchange == 2)) {
			cin.clear();
			cin.ignore(65355, '\n');
			break;
		}
		else {
			cout << "����������������룡" << endl;
			cin.clear();
			cin.ignore(65355, '\n');
		}
	}

	cct_cls();

	int i = 0, ins_all[TASK_NUM + 2], kind_num = 0;

	while (1) {
		if (method == 'A' || method == 'B') {
			if (i >= TASK_NUM)
				break;
		}
		else if (method == 'C') {
			if (kind_num >= TASK_NUM)
				break;
		}
		if (method == 'A') {
			cct_cls();
			cct_gotoxy(0, 0);
			cout << "****************************************************" << endl;
			cout << "*    �ٶ���������水�ֽڱ�ַ                      *" << endl;
			cout << "*    �߼���ַ�ṹ��ҳ��Ϊ20λ��ҳ��ƫ����Ϊ12λ    *" << endl;
			cout << "*    ��ż�ҳ���Ϊ��λ16���ƣ�ҳ�����СΪ4B      *" << endl;
			cout << "*    ����ʼ�����ַΪ0080 0000H                    *" << endl;
			cout << "****************************************************" << endl;
			cct_gotoxy(0, 15);
		}

		ins = cal_instruction(ins, i);
		int page_num = ins / 10;
		int block_tag = ins % 10;  //ҳ��ƫ����
		cout << "����ִ�е�" << setw(3) << ins << "��ָ��  " << "ָ������ҳ��Ϊ" << setw(2) << page_num << "  ��Ӧ���Ϊ " << "008" << (page_num >= 16);
		if (page_num % 16 < 10)
			cout << page_num % 16 << endl;
		else
			cout << char('A' + page_num % 16 - 10) << endl;
		visit(page_table, memory_block, page_table[page_num], block_tag, visit_record, method_of_exchange, loss, method, lru_box, i);

		int tag = 1;
		for (int j = 0; j < kind_num; j++) {
			if (ins_all[j] == ins) {
				tag = 0;
				break;
			}
		}
		if (tag)
			ins_all[kind_num++] = ins;

		if (method == 'A') {
			if (to_be_continued("���س�ִ����һ��ָ��...(����q��ֹ����)"))
				break;
		}
		i++;
	}
	cout << endl;
	cout << "��ǰ����ҳ��ʧ�ܴ���Ϊ : " << loss << endl;
	cout << "��ǰִ��ָ������Ϊ : " << i << endl;
	cout << "ȱҳ��Ϊ : " << (float)((float)loss / (float)i) << endl;
	return 0;
}