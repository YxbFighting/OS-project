#include "image.h"
#include "run.h"
using namespace std;

// ���H!
int main()
{
	cct_setconsoleborder(100, 30, 120, 20000);

	while (1) {
		cct_cls();
		if (run())
			break;
		if (to_be_continued("���س����ز˵�������q��ֹģ�����"))
			break;
	}
	

	return 0;
}