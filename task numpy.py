import numpy as np
import matplotlib.pyplot as plt

# --- creat image ---

img = np.zeros((256,256))
rr, cc = np.ogrid[:256, :256]
circle = (rr - 128)**2 + (cc - 128)**2 < 50**2
img[circle] = 1
img[50:100, 180:220] = 0.7
img[150, 60] = 1
kernel = np.ones((15,15)) / 225
def conv2d(img, kernel):
    pad = kernel.shape[0]//2
    img_pad = np.pad(img, pad)
    out = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            out[i,j] = np.sum(img_pad[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel)
    return out
img += conv2d(np.eye(256)[150][:,np.newaxis], kernel)
img = (img - img.min()) / (img.max() - img.min())

# --- FFT  ---
F_true = np.fft.fft2(img)
mag = np.abs(F_true)
rows, cols = img.shape
Y, X = np.ogrid[:rows, :cols]
mask = (X - cols//2)**2 + (Y - rows//2)**2 < 80**2
F_meas = F_true * mask
mag_meas = np.abs(F_meas)


F_est = mag_meas * np.exp(1j * np.angle(np.fft.fft2(np.random.rand(*img.shape))))
for _ in range(30):
    img_est = np.real(np.fft.ifft2(F_est))
    img_est[img_est<0] = 0
    F_est = mag_meas * np.exp(1j * np.angle(np.fft.fft2(img_est)))

# --- show ---

plt.subplot(1,3,1)
plt.imshow(img, cmap='gray'); plt.title('Ground Truth'); plt.axis('off')
plt.subplot(1,3,2)
plt.imshow(mask, cmap='gray'); plt.title('Mask'); plt.axis('off')
plt.subplot(1,3,3)
plt.imshow(img_est, cmap='gray'); plt.title('Reconstructed'); plt.axis('off')
plt.show()