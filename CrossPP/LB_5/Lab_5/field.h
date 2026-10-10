#ifndef FIELD_H
#define FIELD_H

#include <vector>
#include <cstddef>

class Field
{
public:
    Field() = default;
    Field(int width, int height, int defaultValue = 0)
        : m_width(width), m_height(height),
        m_cells(static_cast<size_t>(width) * height, defaultValue)
    {}

    int width()  const { return m_width; }
    int height() const { return m_height; }

    bool isEmpty() const { return m_width <= 0 || m_height <= 0; }

    int cell(int x, int y) const {
        if (!inBounds(x, y)) return -1;
        return m_cells[static_cast<size_t>(y) * m_width + x];
    }

    void setCell(int x, int y, int value) {
        if (!inBounds(x, y)) return;
        m_cells[static_cast<size_t>(y) * m_width + x] = value;
    }

    void resize(int width, int height, int defaultValue = 0) {
        m_width = width;
        m_height = height;
        m_cells.assign(static_cast<size_t>(width) * height, defaultValue);
    }

    void clear(int defaultValue = 0) {
        std::fill(m_cells.begin(), m_cells.end(), defaultValue);
    }

    const std::vector<int>& cells() const { return m_cells; }
    std::vector<int>&       cells()       { return m_cells; }

private:
    bool inBounds(int x, int y) const {
        return x >= 0 && y >= 0 && x < m_width && y < m_height;
    }

    int m_width  = 0;
    int m_height = 0;
    std::vector<int> m_cells;
};

#endif // FIELD_H