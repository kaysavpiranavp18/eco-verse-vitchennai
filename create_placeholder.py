import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6,4))
ax.text(0.5, 0.5, 'Placeholder Image', ha='center', va='center', fontsize=14)
ax.axis('off')
fig.savefig('fall_detection_dashboard.png')
print('Created fall_detection_dashboard.png')
