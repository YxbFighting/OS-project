#include "image.h"
#include "run.h"
using namespace std;

// 输出H!
int main()
{
	cct_setconsoleborder(100, 30, 120, 20000);

	while (1) {
		cct_cls();
		if (run())
			break;
		if (to_be_continued("按回车返回菜单，输入q终止模拟程序"))
			break;
	}
	

	return 0;
}