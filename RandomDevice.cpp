/*---------------------------------------------------------------------------------*/
/*  COVID SIM - Agent-based model of a pandemic in a population -                  */
/*                                                                                 */
/*  COVID SIM - version 1.0.0 has been created by                                  */
/*                 Khalil Al Handawi           - McGill University                 */
/*                                                                                 */
/*  The copyright of NOMAD - version 3.9.1 is owned by                             */
/*                 Khalil Al Handawi           - McGill University                 */
/*                 Michael Kokkolaras          - McGill University                 */
/*                                                                                 */
/*                                                                                 */
/*  Contact information:                                                           */
/*    McGill University - Systems Optimization Lab (SOL)                           */
/*    Macdonald Engineering Building, 817 Sherbrooke Street West,                  */
/*    Montreal (Quebec) H3A 0C3 Canada                                             */
/*    e-mail: khalil.alhandawi@mail.mcgill.ca                                      */
/*    phone : 1-514-398-2343                                                       */
/*                                                                                 */
/*  This program is free software: you can redistribute it and/or modify it        */
/*  under the terms of the GNU Lesser General Public License as published by       */
/*  the Free Software Foundation, either version 3 of the License, or (at your     */
/*  option) any later version.                                                     */
/*                                                                                 */
/*  This program is distributed in the hope that it will be useful, but WITHOUT    */
/*  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or          */
/*  FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License    */
/*  for more details.                                                              */
/*                                                                                 */
/*  You should have received a copy of the GNU Lesser General Public License       */
/*  along with this program. If not, see <http://www.gnu.org/licenses/>.           */
/*                                                                                 */
/*---------------------------------------------------------------------------------*/

/**
 \file   RandomDevice.cpp
 \brief  Random distribution generator used for simulation (implementation)
 \author Khalil Al Handawi
 \date   2010-08-25
 \see    RandomDevice.h
 */

#include "RandomDevice.h"

/*-----------------------------------------------------------*/
/*                 Random device Constructor                 */
/*-----------------------------------------------------------*/
RandomDevice::RandomDevice(unsigned long n) : rand_seed(n), engine(n) { }

///*-----------------------------------------------------------*/
///*                 Random device Constructor                 */
///*-----------------------------------------------------------*/
//RandomDevice::RandomDevice(unsigned long n)
//{
//	rand_seed = n;
//	engine(n);
//}

/*-----------------------------------------------------------*/
/*              Uniform distribtuion generator               */
/*-----------------------------------------------------------*/
double RandomDevice::randUniform(double low, double high) {
	uniform_real_distribution<float> distribution(low, high);
	return distribution(engine);
}

/*-----------------------------------------------------------*/
/*               Uniform integer distribtuion                */
/*-----------------------------------------------------------*/
int RandomDevice::randUniformInt(int low, int high) {
	uniform_int_distribution<int> distribution(low, high);
	return distribution(engine);
}

/*-----------------------------------------------------------*/
/*              Normal distribtuion generator               */
/*-----------------------------------------------------------*/
double RandomDevice::randNormal(double mean, double std) {
	normal_distribution<float> distribution(mean, std);
	return distribution(engine);
}

/*-----------------------------------------------------------*/
/*      Random uniform distribution for a population         */
/*-----------------------------------------------------------*/
Eigen::ArrayXXf RandomDevice::uniform_dist(double low, double high, int size_x, int size_y)
{

	// uniform distribution with low = low, high = high (using NullaryExpr)
	//default_random_engine generator;
	//Eigen::ArrayXf uniform_vector = Eigen::ArrayXf::NullaryExpr(size_x, size_y, [&]() { return generate_canonical<double, 32>(urng); });
	//uniform_real_distribution<float> dist(low, high);

	auto distribution = [&](float) {return randUniform(low, high); };
	Eigen::ArrayXXf uniform_vector = Eigen::ArrayXXf::NullaryExpr(size_x, size_y, distribution);

	//// normal distribution with mean = mean, stdev = std (using Eigen::Rand)
	//Eigen::Rand::Vmt19937_64 generator;

	//Eigen::ArrayXXf seed_vector{ size_x, size_y };
	//double range = high - low;
	//double mean = (high + low) / 2;
	//Eigen::ArrayXXf uniform_vector = (-range * Eigen::Rand::uniformRealLike(seed_vector, generator)) + mean;

	return uniform_vector;
}

/*-----------------------------------------------------------*/
/*      Normal uniform distribution for a population         */
/*-----------------------------------------------------------*/
Eigen::ArrayXXf RandomDevice::normal_dist(double mean, double std, int size_x, int size_y)
{
	// normal distribution with mean = mean, stdev = std (using NullaryExpr)
	//default_random_engine generator;
	//normal_distribution<> dist(mean, std);
	//auto distribution = [&](double) {return dist(generator); };
	//Eigen::ArrayXXf normal_vector = Eigen::ArrayXf::NullaryExpr(size_x, size_y, distribution);

	auto distribution = [&](float) {return randNormal(mean, std); };
	Eigen::ArrayXXf normal_vector = Eigen::ArrayXXf::NullaryExpr(size_x, size_y, distribution);

	// normal distribution with mean = mean, stdev = std (using Eigen::Rand)
	//Eigen::Rand::Vmt19937_64 generator;

	//Eigen::ArrayXf seed_vector{ size_x, size_y };
	//Eigen::ArrayXf normal_vector = Eigen::Rand::normalLike(seed_vector, generator, mean, std);

	return normal_vector;
}

/*-----------------------------------------------------------*/
/*      Randomly select population members (probability)     */
/*-----------------------------------------------------------*/
Eigen::ArrayXf RandomDevice::Random_choice_prob(int pop_size, double percentage_pop) {
	//fraction of the population that will obey the lockdown
	Eigen::ArrayXf initial_vector = Eigen::ArrayXf::Zero(pop_size, 1);

	//lockdown vector is 1 for those not complying

	Eigen::ArrayXf rand = uniform_dist(0, 1, pop_size, 1);
	Eigen::ArrayXf random_choice_vector = (rand >= percentage_pop).select(initial_vector, 1);

	return random_choice_vector;
}

/*-----------------------------------------------------------*/
/*       Randomly select population members (shuffle)        */
/*-----------------------------------------------------------*/
Eigen::VectorXi RandomDevice::Random_choice(Eigen::ArrayXf input, int n_choices) {
	//fraction of the population that will obey the lockdown

	//auto distribution = [&](int) {return randUniformInt(0, input.rows()); }; // generate a random integer

	//Eigen::VectorXi indices = Eigen::VectorXi::LinSpaced(input.rows(), 0, input.rows());
	//indices = indices.topRows(n_choices);

	vector<int> indices = sequence(0, input.rows(), 1);
	shuffle(indices.begin(), indices.end(), engine);
	indices = slice(indices, 0, n_choices);

	//cout << "in_rows" << input.rows() << endl;

	//cout << "======================" << endl;
	////cout << indices << endl;
	//for (int i = 0; i < indices.size(); i++) {
	//	cout << indices[i] << endl;
	//}
	//cout << "-------------" << endl;
	////cout << input << endl;

 	Eigen::ArrayXf output_f = input(indices);
	Eigen::VectorXi output = output_f.col(0).cast<int>();

	//Eigen::VectorXi output;

	return output;
}

/*-----------------------------------------------------------*/
/*                Randomly generate a number                 */
/*-----------------------------------------------------------*/
double RandomDevice::rand() {
	//fraction of the population that will obey the lockdown
	return randUniform(0.0, 1.0);
}

/*-----------------------------------------------------------*/
/*                  Random device Destructor                 */
/*-----------------------------------------------------------*/
RandomDevice::~RandomDevice()
{
}