# -*- coding: utf-8 -*-

from unittest import IsolatedAsyncioTestCase

from recc_os.storage import Storage


class BaseStorageTestCase(IsolatedAsyncioTestCase):
    async def _setup(self):
        self.host = "localhost"
        self.port = 9000
        self.user = "recc"
        self.pw = "recc1234"
        self.region = ""
        self.secure = False
        self.bucket = "tester"

        self.minio = Storage(
            ss_host=self.host,
            ss_port=self.port,
            ss_user=self.user,
            ss_pw=self.pw,
            ss_region=self.region,
            ss_secure=self.secure,
        )

        await self.minio.open()
        self.assertTrue(self.minio.is_open())

        if await self.minio.exists_bucket(self.bucket):
            await self.minio.remove_bucket(self.bucket, force=True)

    async def asyncSetUp(self):
        try:
            await self._setup()
        except BaseException as e:  # noqa
            print(e)
            await self._teardown()
            raise

    async def _teardown(self):
        if await self.minio.exists_bucket(self.bucket):
            await self.minio.remove_bucket(self.bucket, force=True)
        await self.minio.close()
        self.assertFalse(self.minio.is_open())

    async def asyncTearDown(self):
        await self._teardown()
