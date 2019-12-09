import cv2

cap = cv2.VideoCapture(1)
while True:
	ret, frame = cap.read()
	if ret:
		cv2.imshow('capture',frame)
		if cv2.waitKey(1) & 0xFF == ord('p'):
			cv2.imwrite("img.jpg",frame)
			break

	cv2.imshow("frame", frame)
	k = cv2.waitKey(1) & 0xFF
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()