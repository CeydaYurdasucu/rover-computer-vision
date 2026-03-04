import cv2

# Resmi oku
image = cv2.imread("yazi.webp")

# Griye çevir
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Gürültüyü azaltmak için Gaussian Blur
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Sonuçları göster
cv2.imshow("Orijinal", image)
cv2.imshow("Kenarlar", edges)

cv2.waitKey(0)
cv2.destroyAllWindows()