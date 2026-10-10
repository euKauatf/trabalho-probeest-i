# tests/test_statistics.py

'''
Testes com o unittest (nativo do Python). Pra rodar, na raiz do projeto:
    python -m unittest -v
'''

import os
import random
import statistics
import tempfile
import unittest

from src.models.frequency import ClassInterval
from src.services.reader import read_terminal, read_csv, DataError
from src.services.ungrouped import ungrouped_measures
from src.services.discrete import build_discrete_table, discrete_mean, discrete_median, discrete_mode
from src.services.grouped import (
    sturges, build_class_table, grouped_mean, grouped_median, czuber_mode, king_mode,
    quartile, decile, percentile
)


# Tabela da Parte 3 montada na mão (a mesma do exemplo do enunciado) pra conferir as fórmulas
def manual_table():
    return [
        ClassInterval(18, 22, 32, 32),
        ClassInterval(22, 26, 45, 77),
        ClassInterval(26, 30, 28, 105),
        ClassInterval(30, 34, 15, 120, closed=True),
    ]


class TestReader(unittest.TestCase):
    def test_terminal_ignores_invalid(self):
        values, invalid = read_terminal("1, 2.5, abc, , 4")
        self.assertEqual(values, [1, 2.5, 4])
        self.assertEqual(invalid, ["abc"])

    def test_terminal_without_numbers(self):
        with self.assertRaises(DataError):
            read_terminal("a, b, c")

    def test_csv_with_header_and_semicolon(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "dados.csv")
            with open(path, "w", encoding="utf-8") as file:
                file.write("altura;peso\n1,75;70\n1,80;x\n")
            values, invalid, header = read_csv(path)
        self.assertEqual(values, [1.75, 70, 1.80])
        self.assertEqual(invalid, ["x"])
        self.assertEqual(header, ["altura", "peso"])

    def test_csv_wrong_extension(self):
        with self.assertRaises(DataError):
            read_csv("dados.txt")

    def test_csv_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_csv("nao_existe.csv")


class TestDiscrete(unittest.TestCase):
    # A Parte 2 (tabela) tem que bater com o statistics em qualquer conjunto de dados
    def test_matches_statistics(self):
        random.seed(42)
        for _ in range(200):
            values = [random.randint(0, 30) for _ in range(random.randint(1, 80))]
            table = build_discrete_table(values)
            self.assertAlmostEqual(discrete_mean(table), statistics.mean(values))
            self.assertAlmostEqual(discrete_median(table), statistics.median(values))
            modes = discrete_mode(table)
            if (modes):
                self.assertEqual(sorted(modes), sorted(statistics.multimode(values)))

    def test_table(self):
        table = build_discrete_table([3, 1, 3, 2, 3])
        self.assertEqual([(r.value, r.fi, r.Fi) for r in table], [(1, 1, 1), (2, 1, 2), (3, 3, 5)])

    def test_amodal(self):
        self.assertEqual(discrete_mode(build_discrete_table([1, 2, 3])), [])


class TestGrouped(unittest.TestCase):
    def test_sturges(self):
        self.assertEqual(sturges(120), 8) # 1 + 3.322 · 2.079 = 7.91 -> 8
        self.assertEqual(sturges(50), 7) # 1 + 3.322 · 1.699 = 6.64 -> 7

    # Valores esperados calculados à mão com as fórmulas clássicas
    def test_formulas(self):
        table = manual_table()
        self.assertAlmostEqual(grouped_mean(table), 2984 / 120) # 24.87
        self.assertAlmostEqual(grouped_median(table), 22 + (60 - 32) / 45 * 4) # 24.49
        self.assertAlmostEqual(czuber_mode(table), 22 + 13 / (13 + 17) * 4) # 23.73
        self.assertAlmostEqual(king_mode(table), 22 + 28 / (32 + 28) * 4) # 23.87
        self.assertAlmostEqual(quartile(table, 1), 18 + 30 / 32 * 4) # 21.75
        self.assertAlmostEqual(quartile(table, 3), 26 + (90 - 77) / 28 * 4) # 27.86
        self.assertAlmostEqual(decile(table, 2), 18 + 24 / 32 * 4) # 21.00
        self.assertAlmostEqual(decile(table, 7), 26 + (84 - 77) / 28 * 4) # 27.00
        self.assertAlmostEqual(percentile(table, 15), 18 + 18 / 32 * 4) # 20.25
        self.assertAlmostEqual(percentile(table, 22), 18 + 26.4 / 32 * 4) # 21.30
        self.assertAlmostEqual(percentile(table, 63), 22 + (75.6 - 32) / 45 * 4) # 25.88
        self.assertAlmostEqual(percentile(table, 70), 26 + (84 - 77) / 28 * 4) # 27.00

    def test_every_value_lands_in_a_class(self):
        random.seed(7)
        for _ in range(200):
            values = [round(random.uniform(-50, 50), random.randint(0, 3)) for _ in range(random.randint(1, 150))]
            table, k, total_range, h = build_class_table(values)
            self.assertEqual(table[-1].Fi, len(values))
            self.assertEqual(sum(row.fi for row in table), len(values))

    def test_boundary_goes_to_next_class(self):
        # min 0, max 1, n = 10 -> k = 4, h = 0.25 -> 0.5 tem que cair em [0.50 - 0.75)
        table, k, total_range, h = build_class_table([0, 0.1, 0.2, 0.3, 0.5, 0.5, 0.6, 0.8, 0.9, 1])
        self.assertEqual([row.fi for row in table], [3, 1, 3, 3])

    def test_all_values_equal(self):
        table, k, total_range, h = build_class_table([5, 5, 5])
        self.assertEqual(k, 1)
        self.assertEqual(table[0].fi, 3)
        self.assertAlmostEqual(grouped_mean(table), 5.5)


class TestUngrouped(unittest.TestCase):
    def test_measures(self):
        measures = ungrouped_measures([1, 2, 2, 3, 4])
        self.assertEqual(measures["mean"], 2.4)
        self.assertEqual(measures["median"], 2)
        self.assertEqual(measures["mode"], 2)


if __name__ == "__main__":
    unittest.main()
