function EraseReturnSimbol(s) {
    simbil_position = index(s,"\r");
    if (0 == simbil_position) {
        return s;
    }
    return substr(s, 0, simbil_position-1);
}

BEGIN {
	FS = ";";
	printf("<table>\n");
}

(FNR == 1)&&(NF > 0) {
	printf("\t<tr>\n\t\t");
	for (i = 1; i <= NF; i++) {
		printf("<th>%s</th>",EraseReturnSimbol($(i)));
	}
	printf("\n\t</tr>\n");
}


(FNR > 1)&&(NF > 0) {
	printf("\t<tr>\n\t\t");
	for (i = 1; i <= NF; i++) {
		printf("<td>%s</td>",EraseReturnSimbol($(i)));
	}
	printf("\n\t</tr>\n");
}

END {printf("</table>\n");}