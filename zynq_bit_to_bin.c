#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

#define FPGA_BIN_SIZE (4045564)

int main(int argc, char * argv[])
{
	FILE * sp = NULL;
	FILE * dp = NULL;
	long skip_len = 0;
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
	skip_len = ftell(sp) - FPGA_BIN_SIZE;
	assert(skip_len > 0);
	fseek(sp, skip_len, SEEK_SET);

	content = malloc(FPGA_BIN_SIZE);
	if (!content) {
		printf("malloc failure\n");
		goto exit3;
	}

	ret = fread(content, FPGA_BIN_SIZE, 1, sp);
	if (ret != 1) {
		printf("read %ld error: %ld\n", FPGA_BIN_SIZE, (long)1);
		goto exit4;
	}

	{
		long i = 0;
		char * p = content;
		for (i = 0; i < FPGA_BIN_SIZE; i += 4) {
			char tmp;
			tmp = p[3]; p[3] = p[0]; p[0] = tmp;
			tmp = p[2]; p[2] = p[1]; p[1] = tmp;
			p = &p[4];
		}
	}

	ret = fwrite(content, FPGA_BIN_SIZE, 1, dp);
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
