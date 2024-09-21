
# Afeka Deep Learning Course Project
### Dana Mizrahi, Aviv Salomon, Ben Gornizky and Shany Herskovits

# Topic: Image super resolution using CNN with attention

## Chosen article: 
### Image Super-Resolution Using Very Deep Residual Channel Attention Networks Yulun Zhang, Kunpeng Li, Kai Li, Lichen Wang, Bineng Zhong, and Yun Fu. Jul 2018

### [Link to project code](https://github.com/ShanyHerskovits/Afeka_deep_learning_project)
### Abstract:

Image super-resolution (SR) aims to reconstruct high-resolution (HR) images from low-resolution (LR) inputs, a critical task in fields such as security surveillance, medical imaging, and object recognition. 
With the rise of deep learning, Convolutional Neural Networks (CNNs) have significantly enhanced SR performance. This research focuses on investigating the ability of CNN with an attention mechanism to eliminate distortions in the LR images while performing SR, specifically through the implementation of the Residual Channel Attention Network (RCAN). By leveraging channel attention and residual learning, RCAN is designed to capture and emphasize high-frequency details even in noisy LR images. Using the RealSR V3 dataset, which provides real-world image pairs, we fine-tune the RCAN model across various scaling factors (x2, x4, x8) with the addition of adaptive Gaussian noise to assess the model's robustness. 
Results demonstrate that the model effectively restores detailed HR images from noisy LR inputs, with quantitative evaluation using PSNR and SSIM indicating superior performance compared to the base RCAN model of the same scale. Despite performance degradation at higher scales, the study highlights the effectiveness of CNN-based attention mechanisms in SR, paving the way for further improvements in handling extreme noise and scaling challenges.

[Link to project full report](https://docs.google.com/document/d/1040lQCO0ZybtKqY9-LksMFMvPPoC6tiN/edit?usp=sharing&ouid=105500634718547556077&rtpof=true&sd=true)

[Link to project presentation](https://docs.google.com/presentation/d/1Ao2emv-vTmM-eR85qVnxHAqFlGK0Y-wT/edit?usp=sharing&ouid=105500634718547556077&rtpof=true&sd=true)

[Link to project poster](https://docs.google.com/presentation/d/1YYmRy3RWMa0ngTqubVCHVc7nzmyp77XW/edit?usp=sharing&ouid=105500634718547556077&rtpof=true&sd=true)



