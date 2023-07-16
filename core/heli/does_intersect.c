int does_line_intersect_square(float k, float b, float x1, float y1, float x2, float y2) {
	float y_at_x1 = k * x1 + b;
	float y_at_x2 = k * x2 + b;
	if (y1 <= y_at_x1 && y_at_x1 < y2 || y1 < y_at_x2 && y_at_x2 <= y2)  {
		return 1;
	}
	float x_at_y1 = (y1 - b) / k;
	float x_at_y2 = (y2 - b) / k;
	if (x1 <= x_at_y1 && x_at_y1 < x2 || x1 < x_at_y2 && x_at_y2 <= x2) {
		return 1;
	}
	return 0;
}
