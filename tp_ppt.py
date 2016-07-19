z1 = sur_perimetre[col].reset_index()
z2 = z1[z1[col] > 0]
z3 = z1[z1[col] < 0]
plt.plot(z2[z2.columns[0]], z2[z2.columns[1]],'g.')
ax = plt.gca()
ax.set_axis_bgcolor('white')
plt.plot(z3[z3.columns[0]], z3[z3.columns[1]],'r.')
plt.xticks(rotation=45)
ax.set_title(col)
ax.set_xlabel("date")
ax.set_ylabel("count")
