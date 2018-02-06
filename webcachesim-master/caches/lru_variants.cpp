#include <unordered_map>
#include <random>
#include <cmath>
#include <cassert>
#include "lru_variants.h"
#include "../random_helper.h"
#include <math.h>
#include <fstream>

/*
  LRU: Least Recently Used eviction
*/
bool LRUCache::lookup(SimpleRequest* req)
{
    CacheObject obj(req);
    auto it = _cacheMap.find(obj);
    if (it != _cacheMap.end()) {
        // log hit
        LOG("h", 0, obj.id, obj.size);
        hit(it, obj.size);
        return true;
    }
    return false;
}

void LRUCache::admit(SimpleRequest* req)
{
    const uint64_t size = req->getSize();
    // object feasible to store?
    if (size > _cacheSize) {
        LOG("L", _cacheSize, req->getId(), size);
        return;
    }
    // check eviction needed
    while (_currentSize + size > _cacheSize) {
        evict();
    }
    // admit new object
    CacheObject obj(req);
    _cacheList.push_front(obj);
    _cacheMap[obj] = _cacheList.begin();
    _currentSize += size;
    LOG("a", _currentSize, obj.id, obj.size);
}

void LRUCache::evict(SimpleRequest* req)
{
    CacheObject obj(req);
    auto it = _cacheMap.find(obj);
    if (it != _cacheMap.end()) {
        ListIteratorType lit = it->second;
        LOG("e", _currentSize, obj.id, obj.size);
        _currentSize -= obj.size;
        _cacheMap.erase(obj);
        _cacheList.erase(lit);
    }
}

void LRUCache::evict()
{
    // evict least popular (i.e. last element)
    if (_cacheList.size() > 0) {
        ListIteratorType lit = _cacheList.end();
        lit--;
        CacheObject obj = *lit;
        LOG("e", _currentSize, obj.id, obj.size);
        _currentSize -= obj.size;
        _cacheMap.erase(obj);
        _cacheList.erase(lit);
    }
}

void LRUCache::hit(lruCacheMapType::const_iterator it, uint64_t size)
{
    _cacheList.splice(_cacheList.begin(), _cacheList, it->second);
}

/*
  FIFO: First-In First-Out eviction
*/
void FIFOCache::hit(lruCacheMapType::const_iterator it, uint64_t size)
{
}

/*
  FilterCache (admit only after N requests)
*/
FilterCache::FilterCache()
    : LRUCache(),
      _nParam(2)
{
}

void FilterCache::setPar(std::string parName, std::string parValue) {
    if(parName=="n") {
        const uint64_t n = std::stoull(parValue);
        assert(n>0);
        _nParam = n;
    } else {
        std::cerr << "unrecognized parameter: " << parName << std::endl;
    }
}


bool FilterCache::lookup(SimpleRequest* req)
{
    CacheObject obj(req);
    _filter[obj]++;
    return LRUCache::lookup(req);
}

void FilterCache::admit(SimpleRequest* req)
{
    CacheObject obj(req);
    if (_filter[obj] <= _nParam) {
        return;
    }
    LRUCache::admit(req);
}


/*
  ThLRU: LRU eviction with a size admission threshold
*/
ThLRUCache::ThLRUCache()
    : LRUCache(),
      _sizeThreshold(524288)
{
}

void ThLRUCache::setPar(std::string parName, std::string parValue) {
    if(parName=="t") {
        const double t = stof(parValue);
        assert(t>0);
        _sizeThreshold = pow(2.0,t);
    } else {
        std::cerr << "unrecognized parameter: " << parName << std::endl;
    }
}


void ThLRUCache::admit(SimpleRequest* req)
{
    const uint64_t size = req->getSize();
    // admit if size < threshold
    if (size < _sizeThreshold) {
        LRUCache::admit(req);
    }
}


/*
  ExpLRU: LRU eviction with size-aware probabilistic cache admission
*/
ExpLRUCache::ExpLRUCache()
    : LRUCache(),
      _cParam(262144)
{
}

void ExpLRUCache::setPar(std::string parName, std::string parValue) {
    if(parName=="c") {
        const double c = stof(parValue);
        assert(c>0);
        _cParam = pow(2.0,c);
    } else if (parName == "OPTA" || "OPTA*") {
        //additional parameter like the which file to generate look up unordered mapc
        const std::string tablePath = "../" + parName + "/" + parValue + ".csv";
        //generate loop up map
        ExpLRUCache::generateTable(tablePath);

    } else {
        std::cerr << "unrecognized parameter: " << parName << std::endl;
    }
    
}

//generate loop up map
void ExpLRUCache::generateTable(std::string tablePath)
{
    std::ifstream fin(tablePath);
    std::string line;
    int i = 0;
    while (getline(fin, line))   
    {  
        std::string admitProb = line.erase(line.find_last_not_of(" \t\r\n") + 1);
        double prob = stof(admitProb);
        std::cout << prob <<std::endl;
        //std::pair<std::int,std::double> probPair (i,prob);
        ExpLRUCache::lookUpMap.insert({i, prob});
        i++;  
    }  
}


void ExpLRUCache::admit(SimpleRequest* req)
{
    const double size = req->getSize();
    const double base = 1.25;
    //admit to cache with probablity that is exponentially decreasing with size
    //double admissionProb = exp(-size/ _cParam);
    //do the look up for the prob parameter
    int logSize = static_cast<int>(log10(size)/ log10(base));
    double admissionProb = lookUpMap[logSize];
    std::bernoulli_distribution distribution(admissionProb);
    if (distribution(globalGenerator)) {
        LRUCache::admit(req);
    }
}

