#include <algorithm>
#include <execution>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <numeric>

#include "basis.h"
#include "utils.h"

using namespace std;

int main(int argc, char* argv[]) {
    Clock clk;

    if (argc != 4) {
        cout << "Usage: ./main <basis file> <in path> <out path>.\n";
    }

    constexpr int nr      = 100;
    constexpr int ntheta  = 50;
    constexpr double rmax = 100.0;

    constexpr int nframes   = 801;
    constexpr int framestep = 100;

    constexpr double phi = 0.0;

    constexpr double dr     = rmax / nr;
    constexpr double dtheta = M_PI / (ntheta - 1);

    const string basis_file = argv[1];
    const string in_path    = argv[2];
    const string out_path   = argv[3];

    vector<double> rr(nr);
    generate(std::begin(rr), std::end(rr), [r = 0.0]() mutable {
        const auto cr = r;
        r += dr;
        return cr;
    });

    vector<double> tt(ntheta);
    generate(std::begin(tt), std::end(tt), [th = 0.0]() mutable {
        const auto ct = th;
        th += dtheta;
        return ct;
    });

    Basis basis;

    ifstream basis_file_stream(basis_file);
    basis.read(basis_file_stream);
    basis_file_stream.close();

    vector<pair<string, string>> paths(nframes);
    generate(begin(paths), end(paths), [frame = 0, in_path, out_path]() mutable {
        const string in_file  = in_path + "/dump-" + std::to_string(frame * framestep) + ".dat";
        const string out_file = out_path + "/density-" + std::to_string(frame * framestep) + ".dat";
        ++frame;
        return make_pair(in_file, out_file);
    });

    mutex mtx;

    for_each(execution::par_unseq, begin(paths), end(paths), [&](const auto& p) {
        {
            lock_guard lock(mtx);
            cout << "Reading file: " << p.first << std::endl;
        }

        vector<cdouble> state(basis.functions_number_sph());

        ifstream in(p.first);
        in.ignore(numeric_limits<streamsize>::max(), '\n');
        for (auto& x : state)
            in >> x;
        in.close();

        ofstream out(p.second);
        out << scientific << setprecision(5);
        for (const auto& r : rr) {
            for (const auto& t : tt) {
                const auto basis_vals = basis(r, t, phi);
                const auto val        = inner_product(state.begin(), state.end(), basis_vals.begin(), cdouble(0, 0));
                out << norm(val) << "  ";
            }
            out << '\n';
        }
    });

    cout << " Wall time: " << setprecision(5) << fixed << clk << "\n\n";
    return EXIT_SUCCESS;
}
