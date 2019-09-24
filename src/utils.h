#pragma once

#include <chrono>
#include <iostream>

class Clock {
   public:
    Clock() = default;
    std::chrono::duration<double> restart();
    std::chrono::duration<double> duration() const;

   private:
    std::chrono::time_point<std::chrono::system_clock> _start{std::chrono::system_clock::now()};
};

std::ostream& operator<<(std::ostream& os, const Clock& rhs);