#include <stdio.h>
#include <stdlib.h>

#define SKIP_LEN (16 * 7)

int main(int argc, char * argv[])
{
	FILE * sp = NULL;
	FILE * dp = NULL;
	long len = 0;
	void * content = NULL;
	size_t ret = -1;

	if (argc != 3) {
		printf("usage: %s <srcfile> <destfile>\n", argv[0]);
		return -1;
	}

	sp = fopen(argv[1], "rb");
	if (!sp) {
		printf("can't open source file\n");
		goto exit1;
	}

	dp = fopen(argv[2], "wb");
	if (!dp) {
		printf("can't open dest file\n");
		goto exit2;
	}

	fseek(sp, 0, SEEK_END);
	len = ftell(sp) - SKIP_LEN;
	fseek(sp, SKIP_LEN, SEEK_SET);

	content = malloc(len);
	if (!content) {
		printf("malloc failure\n");
		goto exit3;
	}

	ret = fread(content, len, 1, sp);
	if (ret != 1) {
		printf("read %ld error: %ld\n", len, (long)1);
		goto exit4;
	}

	{
		long i = 0;
		char * p = content;
		for (i = 0; i < len; i += 4) {
			char tmp;
			tmp = p[3]; p[3] = p[0]; p[0] = tmp;
			tmp = p[2]; p[2] = p[1]; p[1] = tmp;
			p = &p[4];
		}
	}

	ret = fwrite(content, len, 1, dp);
	if (ret != 1) {
		printf("write error\n");
		goto exit4;
	}

exit4:
	free(content);
exit3:
	fclose(dp);
exit2:
	fclose(sp);
exit1:
	return 0;
}
