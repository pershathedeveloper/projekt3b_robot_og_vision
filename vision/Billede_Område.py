import cv2
import numpy as np

# 1. Indlæs billedet
image = cv2.imread("Objekter.png")

# 2. Kontrollér, om billedet blev indlæst korrekt
if image is None:
    print("Billedet kunne ikke indlæses. Tjek filnavnet og stien.")
else:
    # 3. Konverter billedet til gråtone
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 4. Anvend en tærskelværdi for at skabe en binær maske
    _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # 5. Find konturerne af objektet
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])

    # 6. Juster x- og y-koordinaterne for at fjerne en del af venstre side og bunden (f.eks. 60 pixels vandret og 120 pixels lodret)
    x_adjusted = x + 100
    y_adjusted = y + 100
    w_adjusted = w - 100
    h_adjusted = h - 235  # Fjerner mere af bunden

    # 7. Isoler objektet ved hjælp af masken
    isolated_object = image[y_adjusted:y_adjusted+h_adjusted, x_adjusted:x_adjusted+w_adjusted]
    isolated_mask = mask[y_adjusted:y_adjusted+h_adjusted, x_adjusted:x_adjusted+w_adjusted]

    # 8. Anvend masken på det isolerede objekt for at fjerne baggrunden
    isolated_object = cv2.bitwise_and(isolated_object, isolated_object, mask=isolated_mask)

    # 9. Opret en ny maske for at sikre, at kun de relevante dele af billedet bliver inkluderet
    final_mask = np.zeros_like(isolated_object)
    final_mask[isolated_mask > 0] = isolated_object[isolated_mask > 0]

    # 10. Vis det isolerede objekt i et vindue
    cv2.imshow("Mit Isolerede Objekt", final_mask)

    # 11. Vent, indtil en tast trykkes, før vinduet lukkes
    cv2.waitKey(0)

    # 12. Luk vinduet
    cv2.destroyAllWindows()