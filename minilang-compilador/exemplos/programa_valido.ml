fator = 3;
total = 1;

for (n = 1; n <= 4; n = n + 1) {
    total = total * fator;
}

while (total > 10) {
    print(total);
    total = total - 3;
}

if (total == 1) {
    print(true);
} else {
    print(false);
}
