#include "catch.hpp"
#include "high_platform_test_helper.hpp"
#include <core/compute_platform/ComputeModule.h>
#include <core/high_platform/PythonComputeModule.h>
#include <core/multidim_image_platform/MultiDimImage.hpp>

using namespace core::high_platform;
using namespace core::compute_platform;
using namespace core::multidim_image_platform;
using namespace std;

namespace high_platform_test {

    vector<shared_ptr<ComputeModule>>
    addGrowingLayer(vector<shared_ptr<ComputeModule>> prevLayer,
        ComputePlatform& p, bool lastLayer)
    {
        vector<shared_ptr<ComputeModule>> result;
        if (prevLayer.empty()) {
            result.push_back(make_shared<ImageSource>(p));
            return result;
        }
        
        if (!lastLayer) {
            auto side1 = make_shared<ImageBypass>(p);
            auto side2 = make_shared<ImageBypass>(p);

            REQUIRE(connectPorts(*prevLayer[0], 0, *side1, 0) == true);
            REQUIRE(connectPorts(*prevLayer[prevLayer.size()-1], 0, *side2, 0) == true);

            result.push_back(side1);
            for (int i = 0; i < (int)prevLayer.size() - 1; ++i) {
                auto m = make_shared<TwoImageBypass>(p);
                result.push_back(m);
                REQUIRE(connectPorts(*prevLayer[i], 0, *m, 0) == true);
                REQUIRE(connectPorts(*prevLayer[i + 1], 0, *m, 1) == true);
            }
            result.push_back(side2);

            return result;
        } else {
            auto side1 = make_shared<ImageSink>(p);
            auto side2 = make_shared<ImageSink>(p);

            REQUIRE(connectPorts(*prevLayer[0], 0, *side1, 0) == true);
            REQUIRE(connectPorts(*prevLayer[prevLayer.size()-1], 0, *side2, 0) == true);

            result.push_back(side1);
            for (int i = 0; i < (int)prevLayer.size() - 1; ++i) {
                auto m = make_shared<TwoImageSink>(p);
                result.push_back(m);
                REQUIRE(connectPorts(*prevLayer[i], 0, *m, 0) == true);
                REQUIRE(connectPorts(*prevLayer[i + 1], 0, *m, 1) == true);
            }
            result.push_back(side2);

            return result;
        }
    }
}

using namespace high_platform_test;

SCENARIO("compute platform works with multidim images", "[core/high_platform]")
{
    GIVEN("a net manipulating multidim images, the nodes forwards its input to the output") {
        ComputePlatform p;
        vector<vector<shared_ptr<ComputeModule>>> modules;
        vector<shared_ptr<ComputeModule>> first;
        modules.push_back(high_platform_test::addGrowingLayer(first, p, false));
        for (int i = 0; i < 3; ++i) {
            auto layer = high_platform_test::addGrowingLayer(modules.back(), p, i == 2);
            modules.push_back(layer);
        }

        // S = source
        // M = module
        // SNK = sink
        //
        // S -> M -> M -> SNK
        // |    |    |
        // v    v    v
        // M -> M -> SNK
        // |    |
        // v    v
        // M -> SNK
        // |
        // v
        // SNK
        //
        // Data should be copied at every junction, and the originals should be carried through
        // resulting in 6 copies and 3 carried 'originals'

        REQUIRE(p.checkCompleteness() == true);

        Image im({64, 64, 3});
        im.at({11, 17, 0}) = 42.0f;
        dynamic_pointer_cast<ImageSource>(modules[0][0])->setImage(im);

        WHEN("running the net") {
            p.run();

            THEN("all the outputs contain the same value") {
                REQUIRE(dynamic_pointer_cast<ImageSink>(modules[3][0])->getImage().at({11, 17, 0}) == 42.0f);
                REQUIRE(dynamic_pointer_cast<TwoImageSink>(modules[3][1])->getImage().at({11, 17, 0}) == 42.0f);
                REQUIRE(dynamic_pointer_cast<TwoImageSink>(modules[3][2])->getImage().at({11, 17, 0}) == 42.0f);
                REQUIRE(dynamic_pointer_cast<ImageSink>(modules[3][3])->getImage().at({11, 17, 0}) == 42.0f);
            }
        }
    }
}

namespace py = pybind11;

SCENARIO("test pybind11 python binding: a3dc.MultiDimImage", "[core/high_platform]")
{
    GIVEN("a MultiDimImage instanced on cpp side") {
        PythonEnvironment::instance();

        MultiDimImage<uint8_t> im({32, 32});
        im.at({17, 19}) = 42;
        WHEN("passed to python side") {
            using namespace py::literals;
            auto locals = py::dict("x"_a = im);
            THEN("it is passed correctly") {
                py::exec(R"(
                    y = x[17, 19] == 42
                )", py::globals(), locals);
                
                bool y = locals["y"].cast<bool>();
                REQUIRE(y == true);
            }
        }
    }

    GIVEN("a MultiDimImage instanced on python side") {
        PythonEnvironment::instance();
        
        auto locals = py::dict();
        py::exec(R"(
            import a3dc
            x = a3dc.MultiDimImageUInt8([16, 16])
            x[7, 9] = 42
        )", py::globals(), locals);
        
        WHEN("passed to the cpp side") {
            THEN("it is passed correctly") {
                auto im = locals["x"].cast<MultiDimImage<uint8_t>>();
                REQUIRE(im.at({7, 9}) == 42);
            }
        }
    }

    // TODO: test: create on cpp side, modify on python side, the instance on cpp is modified too
    // TODO: test: Meta item read/write
}

SCENARIO("high_platform basic usage", "[core/high_platform]")
{
    string codeSource = R"code(
        import a3dc
        import numpy

        a3dc.set_module_args({
            inputs: {},
            outputs: {'out_image': a3dc.types.image}})

        a3dc.set_module_main(module_main)

        def module_main():
            return {'out_image': np.ones((320, 240))}
    )code";

    string codeAdd = R"code(
        import a3dc

        a3dc.set_module_args({
            inputs: {'image1': a3dc.types.image, 'image2': a3dc.types.image},
            outputs: {'out_image': a3dc.types.image}})

        a3dc.set_module_main(module_main)

        def module_main(image1, image2):
            return {'out_image': image1 + image2}
    )code";

    string codeTarget = R"code(
        import a3dc

        a3dc.set_module_args({
            inputs: {'image': a3dc.types.image},
            outputs: {}})

        a3dc.set_module_main(module_main)

        def module_main():
            return None
    )code";

    GIVEN("a simple net") {
        ComputePlatform p;

        // PythonComputeModule src1(p, codeSource);
        // PythonComputeModule src2(p, codeSource);
        // PythonComputeModule add(p, codeAdd);
        // PythonComputeModule dst(p, codeTarget);

        // REQUIRE(p.size() == 3);

        // REQUIRE(src1.outputPort(0).lock()->bind(add.inputPort(0)) == true);
        // REQUIRE(src2.outputPort(0).lock()->bind(add.inputPort(1)) == true);
        // REQUIRE(add.outputPort(0).lock()->bind(dst.inputPort(0)) == true);

        // WHEN("run is called") {
        //     p.run();
        //     THEN("it outputs the correct result") {
        //         //REQUIRE(dd.getResult() == 43);
        //     }
        // }
    }
}